import { Widget } from '@lumino/widgets';
import { tableRowsIcon } from '@jupyterlab/ui-components';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { getFileList, getFileProxyToken } from '../api/project';
import type { IProjectData, IDataset } from '../types';
import DatasetListPanel from '../components/DatasetListPanel';
import ReactDOM from 'react-dom';
import React from 'react';
class DataSetListSidebarWidget extends Widget {
  private listContainer: HTMLElement; // 定义 listContainer 为类的属性
  params: any;
  public projectData: IProjectData;
  datasetList: IDataset[];
  token: any;
  constructor(options: any) {
    super();
    this.addClass('ln-dataset-list-sidebar'); // 使用 ln- 前缀
    this.id = 'ln-dataset-list-dataset';
    this.title.caption = '数据集';
    this.title.label = '数据集';
    this.title.icon = tableRowsIcon;
    this.title.closable = true; // 允许关闭
    this.projectData = options.projectData || {};
    this.datasetList = options.projectData.storageList || [];
    this.listContainer = document.createElement('div');
    this.listContainer.className = 'ln-dataset-list';
    this.node.appendChild(this.listContainer);

    this.params = {
      searchKey: '',
      pageSize: 15,
      pageNum: 1,
      tagLabels: [],
      sortType: 'deployTime'
    };

    // 调用获取版本的函数
    this.getVersions();
  }

  async getToken(id: string) {
    try {
      this.token = await getFileProxyToken({
        expires: 3600,
        businessId: id,
        businessType: 1
      });
    } catch (error) {
      console.error('Error in getToken:', error);
      throw error;
    }
  }

  async queryFileList(dataset: any, token: any) {
    const queryParams = {
      bucketName: dataset.bucketCrName,
      storageType: 'filesystem',
      dir: dataset.bucketPath.slice(1) + '/',
      pageNumber: 1,
      pageSize: 2147483647
    };
    try {
      if (!token) {
        throw new Error('No valid auth token');
      }
      const res = await getFileList(queryParams, token, dataset.clusterId);
      if (res.data?.data.fileList) {
        dataset.fileList = res.data.data.fileList;
      } else {
        console.warn('File list is empty or undefined');
        dataset.fileList = [];
      }
    } catch (error) {
      console.error('Error in getFileListData:', error);
      throw error;
    }
  }

  async getVersions() {
    try {
      await Promise.all(
        this.datasetList.map(async (item: any) => {
          await this.getToken(item.businessId);
          await this.queryFileList(item, this.token);
          console.log(this.datasetList);
        })
      );

      this.updateDatasetList(this.datasetList);
    } catch (error) {
      console.error('请求数据时出错:', error);
      throw error; // 重新抛出错误
    }
  }

  updateDatasetList(data: IDataset[]) {
    ReactDOM.render(
      <div>
        {data.map((dataset, index) => (
          <DatasetListPanel
            key={`${dataset.name}-${index}`}
            title={dataset.name}
            files={dataset.fileList || []}
            onFileClick={fileName => {
              console.log(`Clicked file: ${fileName}`);
            }}
          />
        ))}
      </div>,
      this.listContainer
    );
  }

  install(app: JupyterFrontEnd) {
    app.shell.add(this, 'left', {
      rank: 900,
      type: 'tab'
    });
  }
}

export default DataSetListSidebarWidget;
