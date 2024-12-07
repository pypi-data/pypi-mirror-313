import { IJGISExternalCommandRegistryToken, IJGISFormSchemaRegistryToken, IJGISLayerBrowserRegistryToken, IJupyterGISDocTracker } from '@jupytergis/schema';
import { WidgetTracker } from '@jupyterlab/apputils';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { ITranslator } from '@jupyterlab/translation';
import { JupyterGISExternalCommandRegistry } from './externalcommand';
import { JupyterGISLayerBrowserRegistry } from './layerBrowserRegistry';
import { JupyterGISFormSchemaRegistry } from './schemaregistry';
const NAME_SPACE = 'jupytergis';
export const trackerPlugin = {
    id: 'jupytergis:core:tracker',
    autoStart: true,
    requires: [ITranslator],
    optional: [IMainMenu],
    provides: IJupyterGISDocTracker,
    activate: (app, translator, mainMenu) => {
        const tracker = new WidgetTracker({
            namespace: NAME_SPACE
        });
        console.log('jupytergis:core:tracker is activated!');
        return tracker;
    }
};
export const formSchemaRegistryPlugin = {
    id: 'jupytergis:core:form-schema-registry',
    autoStart: true,
    requires: [],
    provides: IJGISFormSchemaRegistryToken,
    activate: (app) => {
        const registry = new JupyterGISFormSchemaRegistry();
        return registry;
    }
};
export const externalCommandRegistryPlugin = {
    id: 'jupytergis:core:external-command-registry',
    autoStart: true,
    requires: [],
    provides: IJGISExternalCommandRegistryToken,
    activate: (app) => {
        const registry = new JupyterGISExternalCommandRegistry();
        return registry;
    }
};
export const layerBrowserRegistryPlugin = {
    id: 'jupytergis:core:layer-browser-registry',
    autoStart: true,
    requires: [],
    provides: IJGISLayerBrowserRegistryToken,
    activate: (app) => {
        console.log('jupytergis:core:layer-browser-registry is activated');
        const registry = new JupyterGISLayerBrowserRegistry();
        return registry;
    }
};
