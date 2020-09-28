

###### tags: `proposal`, `DevOps`

| title | authors | reviewers | approvers | creation-date | last-updated | status |
| ------ | ------ | --------- | --------- | ------------- | ------------ | ------ |
| DevOps Improvement Proposal Process | @liuyang | @wilson<br>@tudor<br>@kris<br>@eric<br>@md | @wangchun | 2020-09-28 | 2020-09-28 | |

# DevOps Improvement Proposals (DIPs)

A DevOps Improvement Proposal (DIP) is a way to propose, communicate, and coordinate on new efforts or improvements for the standards rules that everyone needs to follow in the daily works and technical options, tools, and projects for choosing and developing. 


## Table of Contents
<!-- toc -->
- [Summary](#summary)
- [Motivation](#motivation)
- [Alternatives](#alternatives)
  - [Gitlab Issues vs. DIPs](#github-issues-vs-keps)
- [Reference](#reference)
<!-- /toc -->

## Summary

A standardized development process for DevOps is proposed, in order to:

- provide a common structure for proposing changes to DevOps
- ensure that the motivation for a change is clear
- persist proposals information in a Version Control System (VCS) for future reference
- reserve Gitlab issues for tracking work in flight, instead of creating "umbrella"<sup>[[1](#reference)]</sup>
  issues
- ensure each participants are successfully able to drive changes to completion while each opinion is adequately
  represented throughout the process

This process is supported by a unit of work called a DevOps Improvement Proposal, or DIP.
A DIP attempts to combine aspects of

- a feature, and effort-tracking document
- an agreement of rules, standardization document 
- a design document

into one file, which is created incrementally in collaboration with one or more
DevOps category.

## Motivation

It is difficult but essential to describe the significance of a problem so that someone working in a different environment can understand<sup>[[2](#reference)]</sup>. As a cross-organization team (such as f2pool and stakefish devops) that shares the infrastructure facility, working beyond a single Gitlab group seems vital to
- understand and communicate upcoming infrastructure changes.
- track the chain of custody for a proposed improvement from conception into implementation.

Without a standardized mechanism for describing related improvements, our talented developers may struggle to think about why we were doing in this why. Additionally, for any infrastructure such as Kubernetes, Docker, Prometheus provision needs a common principle to avoid re-inventing wheels.

The purpose of the DIP process is to reduce the amount of "tribal knowledge" in our team. It aims to enhance communication and discoverability by moving decisions from a smattering of mailing lists, video calls, and hallway conversations into a well-tracked artifact.

## Alternatives
### Gitlab issues vs. DIPs
The use of Gitlab issues when proposing changes does not provide us good facilities for signaling approval or rejection of a proposed change to this team since anyone can open an issue at any time. Additionally, managing a proposed change across multiple projects is somewhat cumbersome as labels and milestones need to be updated every time a change spans. These long-lived Gitlab issues lead to an increasing number of issues open against proposed features, which has become a management problem.

In addition to managing issues over time, searching for text within an issue can be challenging. The flat hierarchy of issues can also make navigation and categorization harder. 


## Reference

1. To mark proposal as complete, all of the features need to be implemented. An umbrella issue is tracking all of these changes. Also there need to be sufficient tests for any of these new features and all existing features and documentation should be completed for all features.
2. [Toward Go 2](https://blog.golang.org/toward-go2), Russ Cox 13 July 2017.