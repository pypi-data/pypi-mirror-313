import { ICollaborativeDrive } from '@jupyter/collaborative-drive';
import { JupyterCadPanel } from '@jupytercad/base';
import { IJCadWorkerRegistryToken, JupyterCadModel } from '@jupytercad/schema';
import { MessageLoop } from '@lumino/messaging';
import { Panel, Widget } from '@lumino/widgets';
import { IJupyterYWidgetManager, JupyterYModel } from 'yjs-widgets';
export const CLASS_NAME = 'jupytercad-notebook-widget';
export class YJupyterCADModel extends JupyterYModel {
}
export class YJupyterCADLuminoWidget extends Panel {
    constructor(options) {
        super();
        this.onResize = () => {
            if (this._jcadWidget) {
                MessageLoop.sendMessage(this._jcadWidget, Widget.ResizeMessage.UnknownSize);
            }
        };
        this.addClass(CLASS_NAME);
        this._jcadWidget = new JupyterCadPanel(options);
        this.addWidget(this._jcadWidget);
    }
}
export const notebookRenderePlugin = {
    id: 'jupytercad:yjswidget-plugin',
    autoStart: true,
    requires: [IJCadWorkerRegistryToken],
    optional: [IJupyterYWidgetManager, ICollaborativeDrive],
    activate: (app, workerRegistry, yWidgetManager, drive) => {
        if (!yWidgetManager) {
            console.error('Missing IJupyterYWidgetManager token!');
            return;
        }
        if (!drive) {
            console.error('Missing ICollaborativeDrive token!');
            return;
        }
        class YJupyterCADModelFactory extends YJupyterCADModel {
            ydocFactory(commMetadata) {
                const { path, format, contentType } = commMetadata;
                const fileFormat = format;
                const sharedModel = drive.sharedModelFactory.createNew({
                    path,
                    format: fileFormat,
                    contentType,
                    collaborative: true
                });
                const jupyterCadDoc = sharedModel;
                this.jupyterCADModel = new JupyterCadModel({
                    sharedModel: jupyterCadDoc
                });
                return this.jupyterCADModel.sharedModel.ydoc;
            }
        }
        class YJupyterCADWidget {
            constructor(yModel, node) {
                this.yModel = yModel;
                this.node = node;
                const widget = new YJupyterCADLuminoWidget({
                    model: yModel.jupyterCADModel,
                    workerRegistry
                });
                // Widget.attach(widget, node);
                MessageLoop.sendMessage(widget, Widget.Msg.BeforeAttach);
                node.appendChild(widget.node);
                MessageLoop.sendMessage(widget, Widget.Msg.AfterAttach);
            }
        }
        yWidgetManager.registerWidget('@jupytercad:widget', YJupyterCADModelFactory, YJupyterCADWidget);
    }
};
