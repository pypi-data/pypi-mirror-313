import { IDict, IJGISFormSchemaRegistry } from '@jupytergis/schema';
export declare class JupyterGISFormSchemaRegistry implements IJGISFormSchemaRegistry {
    constructor();
    registerSchema(name: string, schema: IDict): void;
    has(name: string): boolean;
    getSchemas(): Map<string, IDict>;
    private _registry;
}
