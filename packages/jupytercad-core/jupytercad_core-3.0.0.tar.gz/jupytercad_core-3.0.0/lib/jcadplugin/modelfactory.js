import { JupyterCadModel } from '@jupytercad/schema';
/**
 * A Model factory to create new instances of JupyterCadModel.
 */
export class JupyterCadJcadModelFactory {
    constructor(options) {
        /**
         * Whether the model is collaborative or not.
         */
        this.collaborative = document.querySelectorAll('[data-jupyter-lite-root]')[0] === undefined;
        this._disposed = false;
        this._annotationModel = options.annotationModel;
    }
    /**
     * The name of the model.
     *
     * @returns The name
     */
    get name() {
        return 'jupytercad-jcadmodel';
    }
    /**
     * The content type of the file.
     *
     * @returns The content type
     */
    get contentType() {
        return 'jcad';
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
     * Create a new instance of JupyterCadModel.
     *
     * @returns The model
     */
    createNew(options) {
        const model = new JupyterCadModel({
            sharedModel: options.sharedModel,
            languagePreference: options.languagePreference,
            annotationModel: this._annotationModel
        });
        return model;
    }
}
