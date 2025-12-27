/** @odoo-module **/

import { registry } from "@web/core/registry";
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";

// Custom Logic for GearGuard Form
export class GearGuardFormController extends FormController {
    async setup() {
        super.setup();
        console.log("GearGuard Maintenance System Ready!");
    }

    // Example function to trigger a 'Check' alert like in your diagram
    onCheckHardware() {
        const equipment = this.model.root.data.equipment_id;
        if (!equipment) {
            alert("Please select a piece of Equipment first!");
        }
    }
}

registry.category("views").add("gearguard_form", {
    ...formView,
    Controller: GearGuardFormController,
});