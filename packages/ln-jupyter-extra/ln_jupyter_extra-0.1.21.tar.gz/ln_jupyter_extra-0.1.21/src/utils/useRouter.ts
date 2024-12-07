import { IRouter } from '@jupyterlab/application';
import { URLExt } from '@jupyterlab/coreutils';
import { Signal } from '@lumino/signaling';

// 定义路由参数接口
interface IRouteParams {
  [key: string]: string | null;
}

// 定义路由状态接口
interface IRouteState {
  path: string;
  params: IRouteParams;
  query: IRouteParams;
  fullPath: string;
}

class RouterHook {
  private router: IRouter;
  private _currentRoute: IRouteState;
  private _routeChanged: Signal<RouterHook, IRouteState>;

  constructor(router: IRouter) {
    this.router = router;
    this._routeChanged = new Signal(this);

    // 初始化当前路由状态
    this._currentRoute = this.parseRoute(this.router.current);

    // 监听路由变化
    this.router.routed.connect((_, args) => {
      this._currentRoute = this.parseRoute(args);
      this._routeChanged.emit(this._currentRoute);
    });
  }

  // 获取当前路由状态
  get currentRoute(): IRouteState {
    return this._currentRoute;
  }

  // 路由变化信号
  get routeChanged(): Signal<RouterHook, IRouteState> {
    return this._routeChanged;
  }

  // 解析路由信息
  private parseRoute(location: IRouter.ILocation): IRouteState {
    const { path, request } = location;
    const parsed = URLExt.parse(request);
    const searchParams = new URLSearchParams(parsed.search);

    // 解析查询参数
    const query: IRouteParams = {};
    searchParams.forEach((value, key) => {
      query[key] = value;
    });

    // 解析路径参数 (支持 /path/:param 格式)
    const params: IRouteParams = {};
    const pathSegments = path.split('/');
    pathSegments.forEach((segment, index) => {
      if (segment.startsWith(':')) {
        const paramName = segment.slice(1);
        params[paramName] = pathSegments[index] || null;
      }
    });

    return {
      path,
      params,
      query,
      fullPath: request
    };
  }

  // 监听路由变化
  public onRouteChange(callback: (route: IRouteState) => void): {
    dispose: () => void;
  } {
    const handler = (sender: RouterHook, args: IRouteState) => {
      callback(args);
    };

    this._routeChanged.connect(handler);

    // 返回清理函数
    return {
      dispose: () => {
        this._routeChanged.disconnect(handler);
      }
    };
  }

  // 导航到新路由
  public push(path: string, query?: IRouteParams): void {
    const queryString = query
      ? '?' + new URLSearchParams(query as Record<string, string>).toString()
      : '';
    const newPath = `${path}${queryString}`;

    window.history.pushState(null, '', newPath);
  }

  // 替换当前路由
  public replace(path: string, query?: IRouteParams): void {
    const queryString = query
      ? '?' + new URLSearchParams(query as Record<string, string>).toString()
      : '';
    const newPath = `${path}${queryString}`;

    window.history.replaceState(null, '', newPath);
  }

  // 获取指定参数值
  public getParam(name: string): string | null {
    return (
      this.currentRoute.params[name] || this.currentRoute.query[name] || null
    );
  }

  // 获取所有查询参数
  public getQuery(): IRouteParams {
    return this.currentRoute.query;
  }

  // 获取所有路径参数
  public getParams(): IRouteParams {
    return this.currentRoute.params;
  }

  // 监听特定参数变化
  public watchParam(
    paramName: string,
    callback: (value: string | null) => void
  ): { dispose: () => void } {
    const handler = (sender: RouterHook, route: IRouteState) => {
      const newValue =
        route.params[paramName] || route.query[paramName] || null;
      callback(newValue);
    };

    this._routeChanged.connect(handler);

    return {
      dispose: () => {
        this._routeChanged.disconnect(handler);
      }
    };
  }
}

// 使用示例类
// class ExampleWidget {
//     private router: RouterHook;
//     private disposables: { dispose: () => void }[] = [];

//     constructor(app: JupyterFrontEnd) {
//         this.router = new RouterHook(app);

//         // 监听路由变化
//         this.disposables.push(
//             this.router.onRouteChange((route) => {
//                 console.log('Route changed:', route);
//             })
//         );

//         // 监听特定参数变化
//         this.disposables.push(
//             this.router.watchParam('id', (value) => {
//                 console.log('ID parameter changed:', value);
//                 this.handleIdChange(value);
//             })
//         );
//     }

//     private handleIdChange(id: string | null): void {
//         // 处理 id 参数变化的逻辑
//         console.log('Handling ID change:', id);
//     }

//     // 导航方法示例
//     public navigateToItem(id: string): void {
//         this.router.push('/items', { id });
//     }

//     // 清理资源
//     public dispose(): void {
//         this.disposables.forEach(d => d.dispose());
//     }
// }

export { RouterHook, type IRouteState, type IRouteParams };
