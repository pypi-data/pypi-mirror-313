import { JupyterFrontEnd } from '@jupyterlab/application';
import { IEditorLanguageRegistry } from '@jupyterlab/codemirror';
declare const _default: {
    id: string;
    requires: import("@lumino/coreutils").Token<IEditorLanguageRegistry>[];
    autoStart: boolean;
    activate: (app: JupyterFrontEnd, registry: IEditorLanguageRegistry) => void;
}[];
export default _default;
