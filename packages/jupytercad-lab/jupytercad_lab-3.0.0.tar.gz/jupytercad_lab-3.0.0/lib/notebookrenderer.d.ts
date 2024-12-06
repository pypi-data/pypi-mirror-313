import { IJCadWorkerRegistry, JupyterCadModel } from '@jupytercad/schema';
import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import { Panel } from '@lumino/widgets';
import { JupyterYModel } from 'yjs-widgets';
export interface ICommMetadata {
    create_ydoc: boolean;
    path: string;
    format: string;
    contentType: string;
    ymodel_name: string;
}
export declare const CLASS_NAME = "jupytercad-notebook-widget";
export declare class YJupyterCADModel extends JupyterYModel {
    jupyterCADModel: JupyterCadModel;
}
export declare class YJupyterCADLuminoWidget extends Panel {
    constructor(options: {
        model: JupyterCadModel;
        workerRegistry: IJCadWorkerRegistry;
    });
    onResize: () => void;
    private _jcadWidget;
}
export declare const notebookRenderePlugin: JupyterFrontEndPlugin<void>;
