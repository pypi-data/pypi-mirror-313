import { ConsolePanel, IConsoleTracker } from '@jupyterlab/console';
import { ICollaborativeDrive } from '@jupyter/collaborative-drive';
import { JupyterGISModel, IJupyterGISTracker, IJGISExternalCommandRegistry } from '@jupytergis/schema';
import { IRenderMimeRegistry } from '@jupyterlab/rendermime';
import { IEditorMimeTypeService } from '@jupyterlab/codeeditor';
import { ABCWidgetFactory, DocumentRegistry } from '@jupyterlab/docregistry';
import { CommandRegistry } from '@lumino/commands';
import { JupyterGISWidget } from '@jupytergis/base';
import { ServiceManager } from '@jupyterlab/services';
interface IOptions extends DocumentRegistry.IWidgetFactoryOptions {
    tracker: IJupyterGISTracker;
    commands: CommandRegistry;
    externalCommandRegistry: IJGISExternalCommandRegistry;
    manager?: ServiceManager.IManager;
    contentFactory?: ConsolePanel.IContentFactory;
    mimeTypeService?: IEditorMimeTypeService;
    rendermime?: IRenderMimeRegistry;
    consoleTracker?: IConsoleTracker;
    backendCheck?: () => boolean;
    drive?: ICollaborativeDrive | null;
}
export declare class JupyterGISWidgetFactory extends ABCWidgetFactory<JupyterGISWidget, JupyterGISModel> {
    private options;
    constructor(options: IOptions);
    /**
     * Create a new widget given a context.
     *
     * @param context Contains the information of the file
     * @returns The widget
     */
    protected createNewWidget(context: DocumentRegistry.IContext<JupyterGISModel>): JupyterGISWidget;
    private _commands;
    private _externalCommandRegistry;
    private _backendCheck?;
    private _drive?;
}
export {};
