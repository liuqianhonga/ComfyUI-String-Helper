import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
    name: "ComfyUI-String-Helper.ShowTranslateString",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "ShowTranslateString") {
            // 创建显示文本的函数
            function populate(texts) {
                if (this.widgets) {
                    // 只删除带有特定前缀的 widgets
                    const widgetsToRemove = this.widgets.filter(w => w.name?.startsWith("translated_text_"));
                    for (const widget of widgetsToRemove) {
                        widget.onRemove?.();
                        const index = this.widgets.indexOf(widget);
                        if (index > -1) {
                            this.widgets.splice(index, 1);
                        }
                    }
                }

                // 确保 texts 是数组
                const textArray = Array.isArray(texts) ? texts : [texts];

                // 为每个文本创建一个新的 widget，使用特定的命名前缀
                for (let i = 0; i < textArray.length; i++) {
                    const w = ComfyWidgets["STRING"](this, `translated_text_${i}`, ["STRING", { multiline: true }], app).widget;
                    w.inputEl.readOnly = true;
                    w.inputEl.style.opacity = 0.6;
                    w.value = textArray[i];
                }

                // 调整节点大小
                requestAnimationFrame(() => {
                    const sz = this.computeSize();
                    if (sz[0] < this.size[0]) {
                        sz[0] = this.size[0];
                    }
                    if (sz[1] < this.size[1]) {
                        sz[1] = this.size[1];
                    }
                    this.onResize?.(sz);
                    app.graph.setDirtyCanvas(true, false);
                });
            }

            // 处理执行结果
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                if (message.translated_strings) {
                    populate.call(this, message.translated_strings);
                }
            };

            // 处理配置
            const onConfigure = nodeType.prototype.onConfigure;
            nodeType.prototype.onConfigure = function () {
                onConfigure?.apply(this, arguments);
                if (this.widgets_values?.length) {
                    populate.call(this, this.widgets_values.slice(2));
                }
            };
        }
    }
});
