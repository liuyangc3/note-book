Angular app 在文件 main.ts 通过 bootstrapping `AppModule` 来启动的，
Angular 提供了不同平台的多种启动方式，下面主要介绍2种浏览器平台下的启动选项。

# 使用 Just-in-time (JiT) 编译器的动态 bootstrapping
main.ts
```typescript
// The browser platform with a compiler
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

// The app module
import { AppModule } from './app.module';

// Compile and launch the module
platformBrowserDynamic().bootstrapModule(AppModule);
```
Angular compiler 在浏览器启动后编译 app 然后启动 app。

# 使用 Ahead-Of-time (AoT) 编译器
静态编译可以产生体积更小的 app，启动得更快，尤其是在移动端和网络延时较大的场景。

开启静态编译选项，Angular 编译器运行 ahead-of-time 作为 build 过程的一部分，
并产生了自己的文件中的类工厂的集合。其中包括 AppModuleNgFactory。

使用 AppModuleNgFactory 语法与动态方式很相似：
```typescript
// The browser platform without a compiler
import { platformBrowser } from '@angular/platform-browser';

// The app module factory produced by the static offline compiler
import { AppModuleNgFactory } from './app.module.ngfactory';

// Launch with the app module factory.
platformBrowser().bootstrapModuleFactory(AppModuleNgFactory);
platformBrowserDynamic().bootstrapModule(AppModule);
```
因为 app 已经编译过，无需把 Angular 编译器传入浏览器，也无需在浏览器内编译，代码直接从浏览器下载，体积更小，性能更好。
 
无论 JiT 还是 AoT，编译器都会从 AppModule 源码生成 AppModuleNgFactory 类，
JiT 在浏览器内存里创建类，而 AoT 则是编译为物理文件，然后从 main.ts 导入这个类。

通常来说 AppModule 自己是不知道自己是用什么方式启动的，一旦 main.ts 写好，随着 app 代码增加，也无需修改它。 
