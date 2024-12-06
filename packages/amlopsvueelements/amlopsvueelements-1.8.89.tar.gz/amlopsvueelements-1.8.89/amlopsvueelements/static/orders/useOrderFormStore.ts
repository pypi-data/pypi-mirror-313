import { computed, reactive, ref } from 'vue';
import { defineStore } from 'pinia';
import { mapTails } from '@/helpers/order';
import {
  defaultFuelOrderForm,
  defaultGhOrderForm,
  orderDefaultFormModel
} from '@/constants/order.constants';
import { useOrderStore } from './useOrderStore';

import type { IMappedOrder, IOrder, Nullable } from 'shared/types';

export const useOrderFormStore = defineStore('OrderForm', () => {
  const formModel = reactive<Nullable<IOrder>>(orderDefaultFormModel());
  const formErrors = ref([]);
  const windowWidth = ref(window.innerWidth);
  const orderStore = useOrderStore();
  const airGroupModel = computed(() => orderStore.airGroupModel);
  const fuelGroupModel = computed(() => orderStore.fuelGroupModel);

  const updateOrderType = (isFuel: boolean) => {
    if (isFuel) {
      formModel.gh_order = defaultGhOrderForm();
    } else {
      formModel.fuel_order = defaultFuelOrderForm();
    }
  };

  const validateFirstStep = () => {
    return (
      formModel.type &&
      formModel.company &&
      formModel.client &&
      formModel.status &&
      formModel.location &&
      formModel.currency &&
      formModel.primary_client_contact &&
      (formModel.aircraft || formModel.aircraft_type || formModel.is_any_aircraft) &&
      formModel.flight_type
    );
    // return formModel.type
  };

  const validateSecondStep = () => {
    return (
      formModel.type?.is_gh ||
      (formModel.type?.is_fuel &&
        !formModel.fuel_order?.is_open_release &&
        fuelGroupModel?.value &&
        fuelGroupModel?.value?.length > 1 &&
        fuelGroupModel?.value?.every((el: any) => el.fuel_quantity && el.fuel_uom)) ||
      !fuelGroupModel.value ||
      (fuelGroupModel.value && fuelGroupModel.value.length === 1)
    );
  };

  const mapForm = () => {
    const mappedForm: IMappedOrder = {
      status: formModel.status!.id!,
      aml_selling_company: formModel.company!.id!,
      type: formModel.type!.id!,
      client: formModel.client!.id!,
      location: formModel.location!.id!,
      operator: formModel.operator?.id ?? formModel.client!.id!,
      tails: mapTails(formModel, airGroupModel, fuelGroupModel),
      aircraft_type: formModel.aircraft_type?.id,
      is_any_aircraft: formModel.is_any_aircraft!,
      aircraft_sub_allowed: formModel.aircraft_sub_allowed!,
      callsign: formModel.callsign!,
      is_private: formModel.is_private!,
      flight_type: formModel.flight_type!.code!,
      primary_client_contact: formModel.primary_client_contact?.id ?? null,
      currency: formModel.currency?.id
    };

    if (formModel.type?.is_fuel) {
      mappedForm.fuel_order = {
        is_open_release: formModel.fuel_order!.is_open_release!,
        fuel_category: formModel.fuel_order!.fuel_category!.id!,
        fuel_type: formModel.fuel_order!.fuel_type?.id ?? null,
        fuel_uom:
          airGroupModel.value.length > 1
            ? fuelGroupModel.value[0].fuel_uom.id
            : formModel.fuel_order!.fuel_uom!.id!,
        arrival_datetime: formModel.fuel_order!.arrival_datetime_utc!,
        arrival_datetime_is_local: formModel.fuel_order!.arrival_datetime_is_local!,
        arrival_time_tbc: formModel.fuel_order!.arrival_time_tbc!,
        departure_datetime: formModel.fuel_order!.departure_datetime_utc!,
        departure_datetime_is_local: formModel.fuel_order!.departure_datetime_is_local!,
        departure_time_tbc: formModel.fuel_order!.departure_time_tbc!,
        fueling_on: formModel.fuel_order!.fueling_on!,
        post_pre_minutes: formModel.fuel_order!.post_pre_minutes
      };
      delete mappedForm.gh_order;
      if (!formModel.aircraft) {
        if (airGroupModel.value.length === 1) {
          mappedForm.fuel_order!['fuel_quantity'] = Number(formModel.fuel_order!.fuel_quantity!);
        }
      }
    } else {
      mappedForm.gh_order = {
        mission_type: formModel.gh_order!.mission_type!.id!,
        arrival_datetime: formModel.gh_order!.arrival_datetime_utc!,
        arrival_datetime_is_local: formModel.gh_order!.arrival_datetime_is_local!,
        arrival_time_tbc: formModel.gh_order!.arrival_time_tbc!,
        departure_datetime: formModel.gh_order!.departure_datetime_utc!,
        departure_datetime_is_local: formModel.gh_order!.departure_datetime_is_local!,
        departure_time_tbc: formModel.gh_order!.departure_time_tbc!
      };
      delete mappedForm.fuel_order;
    }
    if (formModel.destination) {
      mappedForm.destination = formModel.destination!.id!;
    } else if (formModel.destination_int_dom) {
      mappedForm.destination_int_dom = formModel.destination_int_dom!.code!;
    } else {
      mappedForm.destination = null;
    }
    return mappedForm;
  };

  return {
    formModel,
    formErrors,
    windowWidth,
    updateOrderType,
    validateFirstStep,
    validateSecondStep,
    mapForm
  };
});
