<template>
  <div v-if="isOpen" class="order-modal submit-delivery-modal">
    <div class="order-modal-wrapper">
      <div ref="target" class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm add-default-classes is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">
                  Submit Delivery Ticket Details
                </div>
                <button @click.stop="emit('modal-close')">
                  <img
                    width="12"
                    height="12"
                    src="../../assets/icons/cross.svg"
                    alt="delete"
                    class="close"
                  />
                </button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper flex flex-col items-center">
                <div
                  v-for="(uplift, upliftIndex) in formModel"
                  :key="upliftIndex"
                  class="uplift-element w-full flex flex-col pb-[1.5rem]"
                >
                  <div class="flex justify-between items-center relative pb-[1rem]">
                    <div>Uplift №{{ (upliftIndex as number) + 1 }}</div>
                    <Button
                      class="dropdown-button"
                      @click="
                        () => {
                          visibility[upliftIndex] = !visibility[upliftIndex];
                        }
                      "
                      ><img
                        :class="{ 'dropdown-button-open': visibility[upliftIndex] }"
                        src="../../assets/icons/chevron-down.svg"
                        alt="hide"
                    /></Button>
                    <div class="uplift-divider"></div>
                  </div>
                  <div v-show="visibility[upliftIndex]" class="visibility-wrap">
                    <SelectField
                      v-model="uplift.aircraft"
                      label-text="Aircraft"
                      placeholder="Select Aircraft"
                      label="full_repr"
                      :errors="getErrors(upliftIndex, 'aircraft')"
                      :options="upliftAircrafts"
                    ></SelectField>
                    <div class="w-full flex gap-x-3 mb-[0.75rem]">
                      <div class="w-6/12 min-w-[132px]">
                        <Label
                          :required="false"
                          label-text="Date & Time of Uplift (UTC)"
                          class="whitespace-nowrap"
                        />
                        <FlatPickr
                          v-if="fromDateTime.length === formModel.length"
                          ref="departureDateRef"
                          :model-value="fromDateTime[upliftIndex].date"
                          :config="{
                            allowInput: true,
                            altInput: true,
                            altFormat: 'Y-m-d',
                            dateFormat: 'Y-m-d'
                          }"
                          @update:model-value="onUpdateDate(upliftIndex, $event, false)"
                        />
                      </div>
                      <div class="flex flex-col w-6/12">
                        <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                        <FlatPickr
                          v-if="fromDateTime.length === formModel.length"
                          :model-value="fromDateTime[upliftIndex].time"
                          placeholder="Time"
                          :config="{
                            altFormat: 'H:i',
                            altInput: true,
                            allowInput: true,
                            noCalendar: true,
                            enableTime: true,
                            time_24hr: true,
                            minuteIncrement: 1
                          }"
                          class="!pr-0"
                          @update:model-value="onUpdateDate(upliftIndex, $event, true)"
                        />
                      </div>
                    </div>
                    <div class="w-full flex gap-3">
                      <InputField
                        v-model="uplift.fuel_quantity"
                        class="w-6/12"
                        :errors="getErrors(upliftIndex, 'fuel_quantity')"
                        label-text="Volume Uplifted"
                        placeholder="Please enter quantity"
                      />
                      <SelectField
                        v-model="uplift.fuel_uom"
                        class="w-6/12"
                        :errors="getErrors(upliftIndex, 'fuel_uom')"
                        label-text="&nbsp;"
                        placeholder=""
                        label="description_plural"
                        :options="fuelQuantityUnits"
                      ></SelectField>
                    </div>
                    <SelectField
                      v-model="uplift.fuel_type"
                      label-text="Fuel Type"
                      :errors="getErrors(upliftIndex, 'fuel_type')"
                      placeholder="Select Fuel Type"
                      label="name"
                      :options="upliftFuelTypes"
                    ></SelectField>
                    <SelectField
                      v-model="uplift.ipa"
                      label-text="IPA"
                      :errors="getErrors(upliftIndex, 'ipa')"
                      placeholder="Select IPA"
                      label="full_repr"
                      :options="upliftIPAs"
                    ></SelectField>
                    <InputField
                      v-model="uplift.callsign"
                      label-text="Callsign"
                      :errors="getErrors(upliftIndex, 'callsign')"
                      placeholder="Enter callsign"
                      @keyup="uppercaseCallsign(upliftIndex)"
                    />
                    <SelectField
                      v-model="uplift.destination"
                      label-text="Destination"
                      :errors="getErrors(upliftIndex, 'destination')"
                      placeholder="Select Destination"
                      label="full_repr"
                      :options="upliftDestinations"
                    ></SelectField>
                    <TextareaField
                      v-model="uplift.comments"
                      class="w-full"
                      :errors="getErrors(upliftIndex, 'comments')"
                      label-text="Comments"
                      placeholder="Please enter comments"
                    />
                    <div class="flex items-center justify-start mb-[0.75rem] gap-3">
                      <button class="modal-button icon" @click="onFileInputClick(upliftIndex)">
                        <img
                          height="20"
                          width="20"
                          :src="getImageUrl('assets/icons/paperclip.svg')"
                          alt="attachment"
                        />
                      </button>
                      <input
                        ref="fileInput"
                        class="hidden"
                        type="file"
                        @change="onChangeFile($event, upliftIndex)"
                      />
                      <p class="text-base whitespace-nowrap font-semibold text-main">
                        {{
                          uplift.ticket?.name
                            ? uplift.ticket?.name.split('.')[0].substring(0, 40) +
                              '.' +
                              uplift.ticket?.name.split('.')[1]
                            : ' Delivery Ticket'
                        }}
                      </p>
                    </div>
                    <div v-show="getErrors(upliftIndex, 'ticket')" class="ticket-error">
                      <span>{{ getErrors(upliftIndex, 'ticket') }}</span>
                    </div>
                  </div>
                </div>
                <div class="w-full flex items-center pb-[0.75rem]">
                  <div class="divider-line"></div>
                  <div class="modal-button add gap-2 cursor-pointer" @click="onAddUplift">
                    <img src="../../assets/icons/plus.svg" alt="add" />
                    Add Another Uplift
                  </div>
                  <div class="divider-line"></div>
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer items-center">
          <Loading v-if="isAddUpliftDetailsPending" class="mr-1" />
          <button
            class="modal-button cancel"
            @click.stop="
              refreshForm();
              emit('modal-close');
            "
          >
            Cancel
          </button>
          <button
            class="modal-button submit"
            :disabled="isAddUpliftDetailsPending"
            @click.stop="onSubmit()"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
import { computed } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import useVuelidate from '@vuelidate/core';
import { storeToRefs } from 'pinia';
import { Button, Loading } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { useUpliftFormStore } from '@/stores/useUpliftFormStore';
import OrderForm from '@/components/forms/OrderForm.vue';
import { useMutationOrderUpliftDetails } from '@/services/mutations/uplift';
import {
  useQueryUpliftAircrafts,
  useQueryUpliftDestinations,
  useQueryUpliftFuelQuantityUnits,
  useQueryUpliftFuelTypes,
  useQueryUpliftIPAs
} from '@/services/queries/uplift';
import { upliftRules } from '@/utils/rulesForForms';
import { getImageUrl } from '@/helpers';
import { notify } from '@/helpers/toast';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  organisationId: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['modal-close', 'modal-submit']);

const fromDateTime = ref([
  {
    date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
    time: ''
  }
]);

const target = ref(null);
const orderStore = useOrderStore();
const order = computed(() => orderStore.order);
const orderId = computed(() => orderStore.order?.id);
const enabled = ref(false);
const upliftFormStore = useUpliftFormStore();
const queryClient = useQueryClient();

const { formModel, formErrors } = storeToRefs(upliftFormStore);
const validationModel = ref([{ form: formModel.value![0] }]);
const v$ = ref([useVuelidate(upliftRules(), validationModel.value![0])]);
const visibility = ref([true]);

const fileInput = ref();

const { data: fuelQuantityUnits } = useQueryUpliftFuelQuantityUnits({ enabled });
const { data: upliftAircrafts } = useQueryUpliftAircrafts(orderId, { enabled });
const { data: upliftDestinations } = useQueryUpliftDestinations(orderId, { enabled });
const { data: upliftIPAs } = useQueryUpliftIPAs(orderId, {
  enabled
});
const { data: upliftFuelTypes } = useQueryUpliftFuelTypes(orderId, { enabled });

const { mutate: addUpliftDetailsMutation, isPending: isAddUpliftDetailsPending } =
  useMutationOrderUpliftDetails();

const onSubmit = async () => {
  const isValid = validateForm();
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error');
  } else {
    const payload = upliftFormStore.mapMultipartForm();
    const body = { orderId: orderId.value!, payload };
    await addUpliftDetailsMutation(body, {
      onSuccess: () => {
        refreshForm();
        queryClient.invalidateQueries({ queryKey: ['fuelUplifts', orderId] });
        emit('modal-close');
      }
    });
  }
};

const validateForm = () => {
  let fullFormValid = true;

  formModel.value.forEach(async (form: any, index: number) => {
    const isValid =
      v$?.value[index]!.value.$errors.length === 0 &&
      v$?.value[index]!.value.$silentErrors.length === 0;
    if (!isValid) {
      formErrors.value[index] =
        v$?.value[index]!.value.$errors.length === 0
          ? v$?.value[index]!.value.$silentErrors
          : v$?.value[index]!.value.$errors;
      fullFormValid = false;
    }
  });
  return fullFormValid;
};

const refreshForm = () => {
  upliftFormStore.resetForm();
  validationModel.value = [{ form: formModel.value![0] }];
  v$.value = [useVuelidate(upliftRules(), validationModel.value![0])];
  fromDateTime.value = [
    {
      date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
      time: ''
    }
  ];
  visibility.value = [true];
};

const uppercaseCallsign = (index: number) => {
  formModel.value[index].callsign = formModel.value[index].callsign!.toUpperCase();
};

const onAddUplift = () => {
  const isValid = validateForm();
  if (!isValid) {
    return notify('Error while adding uplift, form is not valid!', 'error');
  }
  upliftFormStore.addUplift();
  fromDateTime.value.push({
    date: new Date(new Date().getTime() + 24 * 60 * 60 * 1000).toLocaleDateString('en-CA'),
    time: ''
  });
  validationModel.value.push({ form: formModel.value![formModel.value.length - 1] });
  v$.value.push(
    useVuelidate(upliftRules(), validationModel.value[validationModel.value.length - 1])
  );
  visibility.value.push(true);
  populateAircrafts(formModel.value.length - 1);
  populateFuelQuantityUnits(formModel.value.length - 1);
  populateFuelTypes(formModel.value.length - 1);
  populateIpas(formModel.value.length - 1);
  populateCallsign(formModel.value.length - 1);
};

const onChangeFile = (event: any, index: number) => {
  const file = event.target.files[0];
  if (file) {
    formModel.value[index].ticket = file;
  }
};

const onFileInputClick = (index: number) => {
  (fileInput.value?.[index] as HTMLElement).click();
};

const onUpdateDate = (index: number, value: any, isTime: boolean) => {
  isTime ? (fromDateTime.value[index].time = value) : (fromDateTime.value[index].date = value);
  const date = fromDateTime.value[index].date;
  const time = fromDateTime.value[index].time;
  const datetime = new Date(`${date} ${time}`);
  formModel.value[index].datetime_utc = datetime.toISOString();
};

const getErrors = (index: number, property: string) => {
  const indexErrors = formErrors.value?.[index];
  if (indexErrors) {
    const errors = indexErrors.find((error: any) => {
      return error.$property === property;
    })?.$message;
    return errors;
  }
};

const populateAircrafts = (index = 0) => {
  if (
    order?.value?.tails!.length === 1 &&
    upliftAircrafts.value &&
    upliftAircrafts.value[0].id === order?.value?.tails[0].tail_number?.id
  ) {
    formModel.value[index].aircraft = upliftAircrafts.value![0];
  }
};

const populateFuelQuantityUnits = (index = 0) => {
  const uom = fuelQuantityUnits.value!.find(
    (el) => el.id === order?.value?.fuel_order?.fuel_uom?.id
  );
  if (uom) {
    formModel.value[index].fuel_uom = uom;
  }
};

const populateFuelTypes = (index = 0) => {
  const type = upliftFuelTypes.value!.find(
    (el) => el.id === order?.value?.fuel_order?.fuel_type?.id
  );
  if (type) {
    formModel.value[index].fuel_type = type;
  }
};

const populateIpas = (index = 0) => {
  const ipa = upliftIPAs.value!.find((el) => el.id === order?.value?.fuel_order?.ipa?.id);
  if (ipa) {
    formModel.value[index].ipa = ipa;
  }
};

const populateCallsign = (index = 0) => {
  formModel.value[index].callsign = order?.value?.callsign;
};

watch(
  () => upliftAircrafts.value,
  (aircrafts) => {
    aircrafts && populateAircrafts();
  }
);

watch(
  () => fuelQuantityUnits.value,
  (uoms) => {
    uoms && populateFuelQuantityUnits();
  }
);

watch(
  () => upliftFuelTypes.value,
  (types) => {
    types && populateFuelTypes();
  }
);

watch(
  () => upliftIPAs.value,
  (ipas) => {
    ipas && populateIpas();
  }
);

watch(
  () => order.value,
  (order) => {
    if (order) {
      populateCallsign();
    }
  }
);

watch(
  () => [props.organisationId, props.isOpen],
  ([id, isOpen]) => {
    enabled.value = !!(id && isOpen);
  }
);
</script>

<style scoped lang="scss">
.submit-delivery-modal {
  .form-body-wrapper {
    max-height: 500px;
  }
  .modal-button {
    display: flex;
    flex-shrink: 0;
    background-color: rgb(81 93 138);
    padding: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    color: rgb(255 255 255);
    border-radius: 0.5rem;

    &.icon {
      background-color: rgba(240, 242, 252, 1);
      color: rgb(81 93 138);
      padding: 0.75rem;
      border-radius: 0.75rem;
      height: 100%;
    }

    &.add {
      background-color: transparent;
      color: rgba(81, 93, 138, 1);
      width: fit-content;

      img {
        filter: brightness(0) saturate(100%) invert(37%) sepia(12%) saturate(1572%)
          hue-rotate(190deg) brightness(94%) contrast(89%);
      }
    }
  }

  .dropdown-button {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgba(81, 93, 138, 1) !important;
    border-color: transparent !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-[0.5rem] rounded-xl #{!important};

    &-open {
      transform: rotate(180deg);
    }
  }

  .ticket-error {
    font-size: 0.75rem;
    color: rgb(225, 29, 72);
  }

  .divider-line {
    width: 100%;
    min-width: 50px;
    height: 1px;
    border-top: 1px solid rgba(223, 226, 236, 1);
  }

  .uplift-element {
    .uplift-divider {
      position: absolute;
      width: calc(100% + 3rem);
      height: 1px;
      background: rgba(223, 226, 236, 1);
      top: -1rem;
      left: -1.5rem;
    }
    &:first-of-type {
      .uplift-divider {
        display: none;
      }
    }
  }
}
</style>
