dmesg
```
CIFS VFS: Unexpected lookup error -5
```
-5 应该是  
```
#define EIO              5      /* I/O error */
```

首先找到这个报错的位置 fs/cifs/dir.c
```c
struct dentry *
cifs_lookup(struct inode *parent_dir_inode, struct dentry *direntry,
	    struct nameidata *nd)
{
...
			rc = cifs_posix_open(full_path, &newInode, nd->path.mnt,
					parent_dir_inode->i_sb,
					nd->intent.open.create_mode,
					nd->intent.open.flags, &oplock,
					&fileHandle, xid);
			/*
			 * The check below works around a bug in POSIX
			 * open in samba versions 3.3.1 and earlier where
			 * open could incorrectly fail with invalid parameter.
			 * If either that or op not supported returned, follow
			 * the normal lookup.
			 */
			switch (rc) {
			case 0:
				/*
				 * The server may allow us to open things like
				 * FIFOs, but the client isn't set up to deal
				 * with that. If it's not a regular file, just
				 * close it and proceed as if it were a normal
				 * lookup.
				 */
				if (newInode && !S_ISREG(newInode->i_mode)) {
					CIFSSMBClose(xid, pTcon, fileHandle);
					break;
				}
			case -ENOENT:
				posix_open = true;
			case -EOPNOTSUPP:
				break;
			default:
				pTcon->broken_posix_open = true;
			}
		}
		if (!posix_open)
			rc = cifs_get_inode_info_unix(&newInode, full_path,
						parent_dir_inode->i_sb, xid);
	} else
		rc = cifs_get_inode_info(&newInode, full_path, NULL,
				parent_dir_inode->i_sb, xid, NULL);

...
	/*	if it was once a directory (but how can we tell?) we could do
		shrink_dcache_parent(direntry); */
	} else if (rc != -EACCES) {
		cERROR(1, ("Unexpected lookup error %d", rc));
		/* We special case check for Access Denied - since that
		is a common return code */
	}

	kfree(full_path);
	FreeXid(xid);
	return ERR_PTR(rc);
}
```
这里 rc 的值是 -5，一共有三个返回 rc 的函数
```
rc = cifs_posix_open(full_path, &newInode, nd->path.mnt,
					parent_dir_inode->i_sb,
					nd->intent.open.create_mode,
					nd->intent.open.flags, &oplock,
					&fileHandle, xid);

rc = cifs_get_inode_info_unix(&newInode, full_path,
						parent_dir_inode->i_sb, xid);
						
rc = cifs_get_inode_info(&newInode, full_path, NULL,
				parent_dir_inode->i_sb, xid, NULL);	
```
由于是挂载的是 windows 的共享 CIFS， 所以只能是 cifs_get_inode_info
 
fs/cifs/inode.c
```

int cifs_get_inode_info(struct inode **pinode,
	const unsigned char *full_path, FILE_ALL_INFO *pfindData,
	struct super_block *sb, int xid, const __u16 *pfid)
{
	int rc = 0, tmprc;
	struct cifsTconInfo *pTcon;
	struct cifs_sb_info *cifs_sb = CIFS_SB(sb);
	char *buf = NULL;
	bool adjustTZ = false;
	struct cifs_fattr fattr;

	pTcon = cifs_sb->tcon;
	cFYI(1, ("Getting info on %s", full_path));

	if ((pfindData == NULL) && (*pinode != NULL)) {
		if (CIFS_I(*pinode)->clientCanCacheRead) {
			cFYI(1, ("No need to revalidate cached inode sizes"));
			return rc;
		}
	}

	/* if file info not passed in then get it from server */
	if (pfindData == NULL) {
		buf = kmalloc(sizeof(FILE_ALL_INFO), GFP_KERNEL);
		if (buf == NULL)
			return -ENOMEM;
		pfindData = (FILE_ALL_INFO *)buf;

		/* could do find first instead but this returns more info */
		rc = CIFSSMBQPathInfo(xid, pTcon, full_path, pfindData,
			      0 /* not legacy */,
			      cifs_sb->local_nls, cifs_sb->mnt_cifs_flags &
				CIFS_MOUNT_MAP_SPECIAL_CHR);
		/* BB optimize code so we do not make the above call
		when server claims no NT SMB support and the above call
		failed at least once - set flag in tcon or mount */
		if ((rc == -EOPNOTSUPP) || (rc == -EINVAL)) {
			rc = SMBQueryInformation(xid, pTcon, full_path,
					pfindData, cifs_sb->local_nls,
					cifs_sb->mnt_cifs_flags &
					  CIFS_MOUNT_MAP_SPECIAL_CHR);
			adjustTZ = true;
		}
	}

	if (!rc) {
		cifs_all_info_to_fattr(&fattr, (FILE_ALL_INFO *) pfindData,
				       cifs_sb, adjustTZ);
	} else if (rc == -EREMOTE) {
		cifs_create_dfs_fattr(&fattr, sb);
		rc = 0;
	} else {
		goto cgii_exit;
	}

	/*
	 * If an inode wasn't passed in, then get the inode number
	 *
	 * Is an i_ino of zero legal? Can we use that to check if the server
	 * supports returning inode numbers?  Are there other sanity checks we
	 * can use to ensure that the server is really filling in that field?
	 *
	 * We can not use the IndexNumber field by default from Windows or
	 * Samba (in ALL_INFO buf) but we can request it explicitly. The SNIA
	 * CIFS spec claims that this value is unique within the scope of a
	 * share, and the windows docs hint that it's actually unique
	 * per-machine.
	 *
	 * There may be higher info levels that work but are there Windows
	 * server or network appliances for which IndexNumber field is not
	 * guaranteed unique?
	 */
	if (*pinode == NULL) {
		if (cifs_sb->mnt_cifs_flags & CIFS_MOUNT_SERVER_INUM) {
			int rc1 = 0;

			rc1 = CIFSGetSrvInodeNumber(xid, pTcon,
					full_path, &fattr.cf_uniqueid,
					cifs_sb->local_nls,
					cifs_sb->mnt_cifs_flags &
						CIFS_MOUNT_MAP_SPECIAL_CHR);
			if (rc1 || !fattr.cf_uniqueid) {
				cFYI(1, ("GetSrvInodeNum rc %d", rc1));
				fattr.cf_uniqueid = iunique(sb, ROOT_I);
				cifs_autodisable_serverino(cifs_sb);
			}
		} else {
			fattr.cf_uniqueid = iunique(sb, ROOT_I);
		}
	} else {
		fattr.cf_uniqueid = CIFS_I(*pinode)->uniqueid;
	}

	/* query for SFU type info if supported and needed */
	if (fattr.cf_cifsattrs & ATTR_SYSTEM &&
	    cifs_sb->mnt_cifs_flags & CIFS_MOUNT_UNX_EMUL) {
		tmprc = cifs_sfu_type(&fattr, full_path, cifs_sb, xid);
		if (tmprc)
			cFYI(1, ("cifs_sfu_type failed: %d", tmprc));
	}

#ifdef CONFIG_CIFS_EXPERIMENTAL
	/* fill in 0777 bits from ACL */
	if (cifs_sb->mnt_cifs_flags & CIFS_MOUNT_CIFS_ACL) {
		cFYI(1, ("Getting mode bits from ACL"));
		cifs_acl_to_fattr(cifs_sb, &fattr, *pinode, full_path, pfid);
	}
#endif

	/* fill in remaining high mode bits e.g. SUID, VTX */
	if (cifs_sb->mnt_cifs_flags & CIFS_MOUNT_UNX_EMUL)
		cifs_sfu_mode(&fattr, full_path, cifs_sb, xid);

	if (!*pinode) {
		*pinode = cifs_iget(sb, &fattr);
		if (!*pinode)
			rc = -ENOMEM;
	} else {
		cifs_fattr_to_inode(*pinode, &fattr);
	}

cgii_exit:
	kfree(buf);
	return rc;
}
```
函数里 rc 由 CIFSSMBQPathInfo 返回，并且没有直接设置 `rc = -EIO` 的地方，所以应该是 CIFSSMBQPathInfo 里出现的 EIO

fs/cifs/cifssmb.c
```c
int
CIFSSMBQPathInfo(const int xid, struct cifsTconInfo *tcon,
		 const unsigned char *searchName,
		 FILE_ALL_INFO *pFindData,
		 int legacy /* old style infolevel */,
		 const struct nls_table *nls_codepage, int remap)
{
/* level 263 SMB_QUERY_FILE_ALL_INFO */
	TRANSACTION2_QPI_REQ *pSMB = NULL;
	TRANSACTION2_QPI_RSP *pSMBr = NULL;
	int rc = 0;
	int bytes_returned;
	int name_len;
	__u16 params, byte_count;

/* cFYI(1, ("In QPathInfo path %s", searchName)); */
QPathInfoRetry:
	rc = smb_init(SMB_COM_TRANSACTION2, 15, tcon, (void **) &pSMB,
		      (void **) &pSMBr);
	if (rc)
		return rc;

	if (pSMB->hdr.Flags2 & SMBFLG2_UNICODE) {
		name_len =
		    cifsConvertToUCS((__le16 *) pSMB->FileName, searchName,
				     PATH_MAX, nls_codepage, remap);
		name_len++;	/* trailing null */
		name_len *= 2;
	} else {	/* BB improve the check for buffer overruns BB */
		name_len = strnlen(searchName, PATH_MAX);
		name_len++;	/* trailing null */
		strncpy(pSMB->FileName, searchName, name_len);
	}

	params = 2 /* level */ + 4 /* reserved */ + name_len /* includes NUL */;
	pSMB->TotalDataCount = 0;
	pSMB->MaxParameterCount = cpu_to_le16(2);
	/* BB find exact max SMB PDU from sess structure BB */
	pSMB->MaxDataCount = cpu_to_le16(4000);
	pSMB->MaxSetupCount = 0;
	pSMB->Reserved = 0;
	pSMB->Flags = 0;
	pSMB->Timeout = 0;
	pSMB->Reserved2 = 0;
	pSMB->ParameterOffset = cpu_to_le16(offsetof(
	struct smb_com_transaction2_qpi_req, InformationLevel) - 4);
	pSMB->DataCount = 0;
	pSMB->DataOffset = 0;
	pSMB->SetupCount = 1;
	pSMB->Reserved3 = 0;
	pSMB->SubCommand = cpu_to_le16(TRANS2_QUERY_PATH_INFORMATION);
	byte_count = params + 1 /* pad */ ;
	pSMB->TotalParameterCount = cpu_to_le16(params);
	pSMB->ParameterCount = pSMB->TotalParameterCount;
	if (legacy)
		pSMB->InformationLevel = cpu_to_le16(SMB_INFO_STANDARD);
	else
		pSMB->InformationLevel = cpu_to_le16(SMB_QUERY_FILE_ALL_INFO);
	pSMB->Reserved4 = 0;
	pSMB->hdr.smb_buf_length += byte_count;
	pSMB->ByteCount = cpu_to_le16(byte_count);

	rc = SendReceive(xid, tcon->ses, (struct smb_hdr *) pSMB,
			 (struct smb_hdr *) pSMBr, &bytes_returned, 0);
	if (rc) {
		cFYI(1, ("Send error in QPathInfo = %d", rc));
	} else {		/* decode response */
		rc = validate_t2((struct smb_t2_rsp *)pSMBr);

		if (rc) /* BB add auto retry on EOPNOTSUPP? */
			rc = -EIO;
		else if (!legacy && (pSMBr->ByteCount < 40))
			rc = -EIO;	/* bad smb */
		else if (legacy && (pSMBr->ByteCount < 24))
			rc = -EIO;  /* 24 or 26 expected but we do not read
					last field */
		else if (pFindData) {
			int size;
			__u16 data_offset = le16_to_cpu(pSMBr->t2.DataOffset);

			/* On legacy responses we do not read the last field,
			EAsize, fortunately since it varies by subdialect and
			also note it differs on Set vs. Get, ie two bytes or 4
			bytes depending but we don't care here */
			if (legacy)
				size = sizeof(FILE_INFO_STANDARD);
			else
				size = sizeof(FILE_ALL_INFO);
			memcpy((char *) pFindData,
			       (char *) &pSMBr->hdr.Protocol +
			       data_offset, size);
		} else
		    rc = -ENOMEM;
	}
	cifs_buf_release(pSMB);
	if (rc == -EAGAIN)
		goto QPathInfoRetry;

	return rc;
}
```
可以看到有以下几种情况
```
rc = validate_t2((struct smb_t2_rsp *)pSMBr);
if (rc) /* BB add auto retry on EOPNOTSUPP? */
    rc = -EIO;
else if (!legacy && (pSMBr->ByteCount < 40))
    rc = -EIO;	/* bad smb */
else if (legacy && (pSMBr->ByteCount < 24))
    rc = -EIO;  /* 24 or 26 expected but we do not read
            last field */
```

```c
static int validate_t2(struct smb_t2_rsp *pSMB)
{
	int rc = -EINVAL;
	int total_size;
	char *pBCC;

	/* check for plausible wct, bcc and t2 data and parm sizes */
	/* check for parm and data offset going beyond end of smb */
	if (pSMB->hdr.WordCount >= 10) {
		if ((le16_to_cpu(pSMB->t2_rsp.ParameterOffset) <= 1024) &&
		   (le16_to_cpu(pSMB->t2_rsp.DataOffset) <= 1024)) {
			/* check that bcc is at least as big as parms + data */
			/* check that bcc is less than negotiated smb buffer */
			total_size = le16_to_cpu(pSMB->t2_rsp.ParameterCount);
			if (total_size < 512) {
				total_size +=
					le16_to_cpu(pSMB->t2_rsp.DataCount);
				/* BCC le converted in SendReceive */
				pBCC = (pSMB->hdr.WordCount * 2) +
					sizeof(struct smb_hdr) +
					(char *)pSMB;
				if ((total_size <= (*(u16 *)pBCC)) &&
				   (total_size <
					CIFSMaxBufSize+MAX_CIFS_HDR_SIZE)) {
					return 0;
				}
			}
		}
	}
	cifs_dump_mem("Invalid transact2 SMB: ", (char *)pSMB,
		sizeof(struct smb_t2_rsp) + 16);
	return rc;
}
```
这个函数不会返回 true 值，只能是 pSMBr->ByteCount 的情况

pSMBr 的 struct，对应的应该是 SMB response 
```
typedef struct smb_com_transaction2_qpi_rsp {
	struct smb_hdr hdr;	/* wct = 10 + SetupCount */
	struct trans2_resp t2;
	__u16 ByteCount;
	__u16 Reserved2; /* parameter word is present for infolevels > 100 */
} __attribute__((packed)) TRANSACTION2_QPI_RSP;
```
调用 CIFSSMBQPathInfo 是 not legacy
```
rc = CIFSSMBQPathInfo(xid, pTcon, full_path, pfindData,
			      0 /* not legacy */,
...
```
所以应该是 response 字节数 小于 40 字节 出现 EIO
```
else if (!legacy && (pSMBr->ByteCount < 40))
    rc = -EIO;	/* bad smb */
``` 
这里的请求是 CIFSSMBQPathInfo 字面意思是 CIFS SMB Query PATH Info，应该是个 Query 请求

SMB_COM_TRANSACTION2 微软官方定义 https://msdn.microsoft.com/en-us/library/cc246282.aspx

它的 response 结构 https://msdn.microsoft.com/en-us/library/ee441550.aspx





# 2
dmesg
```
CIFS VFS: Autodisabling the use of server inode numbers on \\10.201.30.21\cifs. 
This server doesn't seem to support them properly. 
Hardlinks will not be recognized on this mount. 
Consider mounting with the "noserverino" option to silence this message.
```

定义 fs/cifs/misc.c
```c
void
cifs_autodisable_serverino(struct cifs_sb_info *cifs_sb)
{
	if (cifs_sb->mnt_cifs_flags & CIFS_MOUNT_SERVER_INUM) {
		cifs_sb->mnt_cifs_flags &= ~CIFS_MOUNT_SERVER_INUM;
		cERROR(1, ("Autodisabling the use of server inode numbers on "
			   "%s. This server doesn't seem to support them "
			   "properly. Hardlinks will not be recognized on this "
			   "mount. Consider mounting with the \"noserverino\" "
			   "option to silence this message.",
			   cifs_sb->tcon->treeName));
	}
}
```
fs/cifs/inode.c cifs_get_inode_info
```c
int cifs_get_inode_info(struct inode **pinode,
	const unsigned char *full_path, FILE_ALL_INFO *pfindData,
	struct super_block *sb, int xid, const __u16 *pfid)
{
...
	/*
	 * If an inode wasn't passed in, then get the inode number
	 *
	 * Is an i_ino of zero legal? Can we use that to check if the server
	 * supports returning inode numbers?  Are there other sanity checks we
	 * can use to ensure that the server is really filling in that field?
	 *
	 * We can not use the IndexNumber field by default from Windows or
	 * Samba (in ALL_INFO buf) but we can request it explicitly. The SNIA
	 * CIFS spec claims that this value is unique within the scope of a
	 * share, and the windows docs hint that it's actually unique
	 * per-machine.
	 *
	 * There may be higher info levels that work but are there Windows
	 * server or network appliances for which IndexNumber field is not
	 * guaranteed unique?
	 */
	if (*pinode == NULL) {
		if (cifs_sb->mnt_cifs_flags & CIFS_MOUNT_SERVER_INUM) {
			int rc1 = 0;

			rc1 = CIFSGetSrvInodeNumber(xid, pTcon,
					full_path, &fattr.cf_uniqueid,
					cifs_sb->local_nls,
					cifs_sb->mnt_cifs_flags &
						CIFS_MOUNT_MAP_SPECIAL_CHR);
			if (rc1 || !fattr.cf_uniqueid) {
				cFYI(1, ("GetSrvInodeNum rc %d", rc1));
				fattr.cf_uniqueid = iunique(sb, ROOT_I);
				cifs_autodisable_serverino(cifs_sb);
			}
...
```