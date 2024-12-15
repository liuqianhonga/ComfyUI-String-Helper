import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI-String-Helper.StringFormatter",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "StringFormatter") {
            const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);

				if (this.widgets) {
					const pos = this.widgets.findIndex((w) => w.name === "formatted_text");
					if (pos !== -1) {
						for (let i = pos; i < this.widgets.length; i++) {
							this.widgets[i].onRemove?.();
						}
						this.widgets.length = pos;
					}
				}

				const widget = ComfyWidgets["STRING"](this, "formatted_text", ["STRING", { multiline: true }], app).widget;
				widget.inputEl.readOnly = true;
				widget.inputEl.style.opacity = 0.6;
				widget.value = message.formatted_string?.[0] ?? "";

				this.onResize?.(this.size);
			};
        }
    }
});
