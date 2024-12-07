import { ICollaborativeDrive } from '@jupyter/collaborative-drive';
import { JupyterGISPanel } from '@jupytergis/base';
import { JupyterGISModel } from '@jupytergis/schema';
import { MessageLoop } from '@lumino/messaging';
import { Panel, Widget } from '@lumino/widgets';
import { IJupyterYWidgetManager, JupyterYModel } from 'yjs-widgets';
export const CLASS_NAME = 'jupytergis-notebook-widget';
export class YJupyterGISModel extends JupyterYModel {
}
export class YJupyterGISLuminoWidget extends Panel {
    constructor(options) {
        super();
        this.onResize = () => {
            if (this._jgisWidget) {
                MessageLoop.sendMessage(this._jgisWidget, Widget.ResizeMessage.UnknownSize);
            }
        };
        this.addClass(CLASS_NAME);
        this._jgisWidget = new JupyterGISPanel(options);
        this.addWidget(this._jgisWidget);
    }
}
export const notebookRenderePlugin = {
    id: 'jupytergis:yjswidget-plugin',
    autoStart: true,
    optional: [IJupyterYWidgetManager, ICollaborativeDrive],
    activate: (app, yWidgetManager, drive) => {
        if (!yWidgetManager) {
            console.error('Missing IJupyterYWidgetManager token!');
            return;
        }
        if (!drive) {
            console.error('Cannot setup JupyterGIS Python API without a collaborative drive');
            return;
        }
        class YJupyterGISModelFactory extends YJupyterGISModel {
            ydocFactory(commMetadata) {
                const { path, format, contentType } = commMetadata;
                const fileFormat = format;
                const sharedModel = drive.sharedModelFactory.createNew({
                    path,
                    format: fileFormat,
                    contentType,
                    collaborative: true
                });
                this.jupyterGISModel = new JupyterGISModel({
                    sharedModel: sharedModel
                });
                return this.jupyterGISModel.sharedModel.ydoc;
            }
        }
        class YJupyterGISWidget {
            constructor(yModel, node) {
                this.yModel = yModel;
                this.node = node;
                const widget = new YJupyterGISLuminoWidget({
                    model: yModel.jupyterGISModel
                });
                // Widget.attach(widget, node);
                MessageLoop.sendMessage(widget, Widget.Msg.BeforeAttach);
                node.appendChild(widget.node);
                MessageLoop.sendMessage(widget, Widget.Msg.AfterAttach);
            }
        }
        yWidgetManager.registerWidget('@jupytergis:widget', YJupyterGISModelFactory, YJupyterGISWidget);
    }
};
