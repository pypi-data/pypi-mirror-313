import React, { useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';

interface IDatasetListPanelProps {
  title: string;
  files: { fileName: string }[];
  onFileClick?: (fileName: string) => void;
}

const DatasetListPanel: React.FC<IDatasetListPanelProps> = ({
  title,
  files,
  onFileClick = fileName => console.log(`Clicked file: ${fileName}`)
}) => {
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <div className="ln-dataset-list-panel">
      <div
        className="panel-header"
        onClick={() => setIsExpanded(prev => !prev)}
      >
        <div className="panel-title">{title}</div>
        {isExpanded ? (
          <ChevronDown size={18} className="icon" />
        ) : (
          <ChevronRight size={18} className="icon" />
        )}
      </div>
      {isExpanded && (
        <ul className="file-list">
          {files.length > 0 ? (
            files.map((file, index) => (
              <li
                key={`${file.fileName}-${index}`}
                className="file-item"
                onClick={() => onFileClick(file.fileName)}
              >
                {file.fileName}
              </li>
            ))
          ) : (
            <li className="no-files">暂无文件</li>
          )}
        </ul>
      )}
    </div>
  );
};

export default DatasetListPanel;
