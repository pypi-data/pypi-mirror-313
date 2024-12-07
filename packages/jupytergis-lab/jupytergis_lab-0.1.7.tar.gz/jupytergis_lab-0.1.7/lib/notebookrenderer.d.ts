import { JupyterGISModel } from '@jupytergis/schema';
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
export declare const CLASS_NAME = "jupytergis-notebook-widget";
export declare class YJupyterGISModel extends JupyterYModel {
    jupyterGISModel: JupyterGISModel;
}
export declare class YJupyterGISLuminoWidget extends Panel {
    constructor(options: {
        model: JupyterGISModel;
    });
    onResize: () => void;
    private _jgisWidget;
}
export declare const notebookRenderePlugin: JupyterFrontEndPlugin<void>;
