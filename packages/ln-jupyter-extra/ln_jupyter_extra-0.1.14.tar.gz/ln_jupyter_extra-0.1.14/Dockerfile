# 使用官方JupyterLab基础镜像
FROM jupyter/base-notebook:latest

# 先卸载默认版本的 JupyterLab
RUN pip uninstall -y jupyterlab && \
    pip install jupyterlab==4.3.1  # 替换为需要的版本

COPY ./dist/ln_jupyter_extra-0.1.13-py3-none-any.whl ln_jupyter_extra-0.1.13-py3-none-any.whl
#COPY ./schema/variable-inspector-settings.json /opt/conda/share/jupyter/lab/schemas/leinao_jupyter/variable-inspector-settings.json

RUN pip uninstall ln_jupyter_extra \
 && pip install ln_jupyter_extra-0.1.13-py3-none-any.whl

#RUN pip install jupyterlab-language-pack-zh-CN

# 切换回默认的jovyan用户
USER jovyan

# 设置工作目录
WORKDIR /home/jovyan/work

# 暴露JupyterLab默认端口
EXPOSE 8888

# 启动JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root","--NotebookApp.token=''"]