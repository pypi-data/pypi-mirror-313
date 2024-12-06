import { pixelsPerRem } from "../app";
import { componentsById } from "../componentManagement";
import { ComponentId } from "../dataModels";
import { Debouncer } from "../debouncer";
import { callRemoteMethodDiscardResponse } from "../rpc";
import { getAllocatedHeightInPx, getAllocatedWidthInPx } from "../utils";
import { ComponentBase, ComponentState } from "./componentBase";

let notifyBackendOfWindowSizeChange = new Debouncer({
    callback: (width: number, height: number) => {
        try {
            callRemoteMethodDiscardResponse("onWindowSizeChange", {
                newWidth: width,
                newHeight: height,
            });
        } catch (e) {
            console.warn(`Couldn't notify backend of window resize: ${e}`);
        }
    },
});

export type FundamentalRootComponentState = ComponentState & {
    _type_: "FundamentalRootComponent-builtin";
    content: ComponentId;
    connection_lost_component: ComponentId;
    dev_tools: ComponentId | null;
};

export class FundamentalRootComponent extends ComponentBase {
    declare state: Required<FundamentalRootComponentState>;

    public overlaysContainer: HTMLElement;

    private userRootContainer: HTMLElement;
    private connectionLostPopupContainer: HTMLElement;
    private devToolsContainer: HTMLElement;

    createElement(): HTMLElement {
        let element = document.createElement("div");
        element.classList.add("rio-fundamental-root-component");

        element.innerHTML = `
            <div class="rio-user-root-container-outer">
                <div>
                    <div class="rio-user-root-container-inner"></div>
                </div>
            </div>
            <div class="rio-overlays-container"></div>
            <div class="rio-connection-lost-popup-container"></div>
            <div class="rio-dev-tools-container"></div>
        `;

        this.overlaysContainer = element.querySelector(
            ".rio-overlays-container"
        ) as HTMLElement;

        this.userRootContainer = element.querySelector(
            ".rio-user-root-container-inner"
        ) as HTMLElement;
        this.connectionLostPopupContainer = element.querySelector(
            ".rio-connection-lost-popup-container"
        ) as HTMLElement;
        this.devToolsContainer = element.querySelector(
            ".rio-dev-tools-container"
        ) as HTMLElement;

        // Watch for window size changes. This differs between debug mode and
        // release mode. If the dev sidebar is visible, it must be subtracted
        // from the window size. Scrolling also works differently: In release
        // mode we let the browser scroll, but in debug mode we scroll only the
        // user content, and not the sidebar.
        //
        // In debug mode, we can simply attach a ResizeObserver to the element
        // that contains (and scrolls) the user content. But in release mode
        // that element doesn't scroll, so we must obtain the actual window
        // size.
        if (globalThis.RIO_DEBUG_MODE) {
            let outerUserRootContainer = element.querySelector(
                ".rio-user-root-container-outer"
            ) as HTMLElement;
            new ResizeObserver(() => {
                // Notify the backend of the new size
                notifyBackendOfWindowSizeChange.call(
                    getAllocatedWidthInPx(outerUserRootContainer) /
                        pixelsPerRem,
                    getAllocatedHeightInPx(outerUserRootContainer) /
                        pixelsPerRem
                );
            }).observe(outerUserRootContainer);
        } else {
            window.addEventListener("resize", () => {
                notifyBackendOfWindowSizeChange.call(
                    window.innerWidth / pixelsPerRem,
                    window.innerHeight / pixelsPerRem
                );
            });
        }

        return element;
    }

    updateElement(
        deltaState: FundamentalRootComponentState,
        latentComponents: Set<ComponentBase>
    ): void {
        super.updateElement(deltaState, latentComponents);

        // User components
        if (deltaState.content !== undefined) {
            this.replaceOnlyChild(
                latentComponents,
                deltaState.content,
                this.userRootContainer
            );
        }

        // Connection lost popup
        if (deltaState.connection_lost_component !== undefined) {
            this.replaceOnlyChild(
                latentComponents,
                deltaState.connection_lost_component,
                this.connectionLostPopupContainer
            );
        }

        // Dev tools sidebar
        if (deltaState.dev_tools !== undefined) {
            this.replaceOnlyChild(
                latentComponents,
                deltaState.dev_tools,
                this.devToolsContainer
            );

            if (deltaState.dev_tools !== null) {
                let devTools = componentsById[deltaState.dev_tools]!;
                devTools.element.classList.add("rio-dev-tools");
            }

            // Enable or disable the user content scroller depending on whether
            // there are dev-tools
            this.element.dataset.hasDevTools = `${
                deltaState.dev_tools !== null
            }`;
        }
    }
}
