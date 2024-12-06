import React from 'react';
import { Notification } from '@jupyterlab/apputils';
import dayjs from 'dayjs';
import { loadProjectVersion } from '../api/project';
import { JupyterFrontEnd } from '@jupyterlab/application';
interface IVersion {
  id: string;
  version: string;
  createTime: string;
  app: JupyterFrontEnd;
}

export const VersionList: React.FC<IVersion> = ({
  id,
  version,
  createTime,
  app
}) => {
  const handleVersionClick = async (id: string) => {
    try {
      await loadProjectVersion({
        versionId: id,
        projectId: localStorage.getItem('projectId') || ''
      });
      // 刷新工作区域
      await refreshFn(app);
    } catch (e) {
      Notification.error('加载失败', { autoClose: 3000 });
      console.log(e);
    }
  };

  const refreshFn = async (app: JupyterFrontEnd) => {
    // 使用传入的 app 实例
    for (const widget of app.shell.widgets('main')) {
      widget.close();
    }

    await app.commands.execute('filebrowser:refresh');

    Notification.success('版本加载成功', { autoClose: 3000 });
  };

  return (
    <div className="ln-version-list-item">
      <div>
        <div className="ln-version-list-item__name">{version}</div>
        <div className="ln-version-list-item__time">
          {dayjs(createTime).format('YYYY-MM-DD HH:mm:ss')}
        </div>
      </div>
      <div
        className="ln-version-list-item__btn"
        onClick={() => handleVersionClick(id)}
      >
        加载版本
      </div>
    </div>
  );
};
