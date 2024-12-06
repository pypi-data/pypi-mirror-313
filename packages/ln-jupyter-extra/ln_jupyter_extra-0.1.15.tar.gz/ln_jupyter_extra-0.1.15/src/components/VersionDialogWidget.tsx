import { ReactWidget } from '@jupyterlab/ui-components';
import React, { useState } from 'react';

// interface VersionDialogWidgetProps {
//   onConfirm: (name: string, description: string) => void;
//   onCancel: () => void;
// }

export class VersionDialogWidget extends ReactWidget {
  constructor(
    private onConfirm: (name: string, description: string) => void,
    private onCancel: () => void
  ) {
    super();
  }

  protected render(): React.ReactElement<any> {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [nameError, setNameError] = useState('');
    const [descError, setDescError] = useState('');

    const validateName = (value: string) => {
      const chineseRegex = /^[\u4e00-\u9fa5a-zA-Z0-9]+$/;
      if (!value) {
        setNameError('版本名称不能为空');
        return false;
      }
      if (value.length > 10) {
        setNameError('版本名称不能超过10个字符');
        return false;
      }
      if (!chineseRegex.test(value)) {
        setNameError('版本名称只能包含中英文和数字');
        return false;
      }
      setNameError('');
      return true;
    };

    const validateDescription = (value: string) => {
      if (value.length > 300) {
        setDescError('版本描述不能超过300个字符');
        return false;
      }
      setDescError('');
      return true;
    };

    const handleSubmit = () => {
      const isNameValid = validateName(name);
      const isDescValid = validateDescription(description);

      if (isNameValid && isDescValid) {
        this.onConfirm(name, description);
      }
    };

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div>
          <label>版本名称:</label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            placeholder="请输入版本名称"
          />
          {nameError && <div style={{ color: 'red' }}>{nameError}</div>}
        </div>
        <div>
          <label>版本描述:</label>
          <textarea
            value={description}
            onChange={e => setDescription(e.target.value)}
            placeholder="请输入版本描述"
          />
          {descError && <div style={{ color: 'red' }}>{descError}</div>}
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button onClick={this.onCancel}>取消</button>
          <button onClick={handleSubmit}>确认</button>
        </div>
      </div>
    );
  }
}
