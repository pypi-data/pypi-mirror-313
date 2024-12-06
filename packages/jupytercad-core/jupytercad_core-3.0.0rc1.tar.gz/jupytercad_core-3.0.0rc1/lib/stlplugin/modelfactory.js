import { JupyterCadModel } from '@jupytercad/schema';
import { JupyterCadStlDoc } from './model';
class JupyterCadStlModel extends JupyterCadModel {
    fromString(data) {
        this.sharedModel.source = data;
        this.dirty = true;
    }
    createSharedModel() {
        return JupyterCadStlDoc.create();
    }
}
/**
 * A Model factory to create new instances of JupyterCadSTLModel.
 */
export class JupyterCadStlModelFactory {
    constructor() {
        /**
         * Whether the model is collaborative or not.
         */
        this.collaborative = document.querySelectorAll('[data-jupyter-lite-root]')[0] === undefined;
        this._disposed = false;
    }
    /**
     * The name of the model.
     *
     * @returns The name
     */
    get name() {
        return 'jupytercad-stlmodel';
    }
    /**
     * The content type of the file.
     *
     * @returns The content type
     */
    get contentType() {
        return 'stl';
    }
    /**
     * The format of the file.
     *
     * @returns the file format
     */
    get fileFormat() {
        return 'text';
    }
    /**
     * Get whether the model factory has been disposed.
     *
     * @returns disposed status
     */
    get isDisposed() {
        return this._disposed;
    }
    /**
     * Dispose the model factory.
     */
    dispose() {
        this._disposed = true;
    }
    /**
     * Get the preferred language given the path on the file.
     *
     * @param path path of the file represented by this document model
     * @returns The preferred language
     */
    preferredLanguage(path) {
        return '';
    }
    /**
     * Create a new instance of JupyterCadSTLModel.
     *
     * @returns The model
     */
    createNew(options) {
        const model = new JupyterCadStlModel({
            sharedModel: options.sharedModel,
            languagePreference: options.languagePreference
        });
        return model;
    }
}
