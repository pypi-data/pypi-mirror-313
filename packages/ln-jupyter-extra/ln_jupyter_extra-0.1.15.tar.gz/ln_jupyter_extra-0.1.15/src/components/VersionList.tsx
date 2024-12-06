import React from 'react';
import { Notification } from '@jupyterlab/apputils';
import dayjs from 'dayjs';

interface IVersion {
  version: string;
  createTime: string;
}

export const VersionList: React.FC<IVersion> = ({ version, createTime }) => {
  const handleVersionClick = () => {
    Notification.success(`加载版本: ${version}`);
  };

  return (
    <div className="ln-version-list-item">
      <div>
        <div className="ln-version-list-item__name">{version}</div>
        <div className="ln-version-list-item__time">
          {dayjs(createTime).format('YYYY-MM-DD HH:mm:ss')}
        </div>
      </div>
      <div className="ln-version-list-item__btn" onClick={handleVersionClick}>
        加载版本
      </div>
    </div>
  );
};
