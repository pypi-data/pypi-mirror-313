<template>
  <div
    v-for="(newService, index) in newServices"
    :key="newService.timestamp"
    class="handling-step-content-element new-service-element-wrap flex"
  >
    <div
      class="handling-step-content-element-wrap flex py-[0.5rem] pl-[0.75rem] el-border-light"
      :class="{
        'w-8/12 gap-2': props.currentTab === 1,
        'w-6/12': props.currentTab === 2
      }"
    >
      <div
        class="handling-step-content-element-el-name flex justify-center items-center w-6/12 pr-4"
      >
        <SelectField
          class="w-full mb-0"
          :is-white="true"
          placeholder="Choose Service"
          :options="displayServices"
          label="name"
          :model-value="newService.name"
          @update:model-value="onSelectNewService($event, index)"
          @search="handleServiceSearch($event)"
        />
      </div>
      <div class="handling-step-content-element-el flex justify-start items-center w-6/12">
        <div class="input-wrap flex items-center pr-[0.75rem] grow">
          <span class="text-light-subtitle pr-[0.5rem] text-[0.75rem]">x</span>
          <InputField
            v-if="newService.is_allowed_free_text"
            :model-value="newService.quantity"
            class="w-full mb-0"
            is-white
            placeholder=" "
            @update:model-value="
              (value) => {
                newService.quantity = value;
              }
            "
          />
          <div
            v-else-if="newService.is_allowed_quantity_selection"
            class="input-wrap flex w-full items-center"
          >
            <InputField
              :model-value="(newService.quantity_value) as string"
              class="w-6/12 mb-0"
              is-white
              is-half
              placeholder=" "
              @update:model-value="
                (value) => {
                  newService.quantity_value = value;
                }
              "
            />
            <SelectField
              class="w-6/12 mb-0"
              :is-white="true"
              :is-half="true"
              placeholder=" "
              disabled
              label="description_plural"
              :model-value="newService.quantity_selection_uom?.description_plural"
            />
          </div>
          <div v-else>--</div>
        </div>
      </div>
    </div>
    <div
      class="handling-step-content-element-wrap flex el-border-light"
      :class="{
        'w-4/12 gap-2 pl-[0.75rem]': props.currentTab === 1,
        'w-6/12': props.currentTab === 2
      }"
    >
      <div
        class="handling-step-content-element-el-name flex justify-center items-center"
        :class="{
          'w-6/12': props.currentTab === 1,
          'w-full': props.currentTab === 2
        }"
      >
        <CheckboxField
          v-model="newService.applies_on_arrival"
          class="mb-0"
          :class="{
            'mr-1': props.currentTab === 1
          }"
          :size="'20px'"
          :background-color="'#fbfcfe'"
          :disabled="!newService.is_arr_available || !newService.name"
        ></CheckboxField>
      </div>
      <div
        class="handling-step-content-element-el flex justify-center items-center"
        :class="{
          'w-6/12': props.currentTab === 1,
          'w-full el-border-light': props.currentTab === 2
        }"
      >
        <CheckboxField
          v-model="newService.applies_on_departure"
          class="mb-0"
          :class="{
            'mr-1': props.currentTab === 1
          }"
          :size="'20px'"
          :background-color="'#fbfcfe'"
          :disabled="!newService.is_dep_available || !newService.name"
        ></CheckboxField>
      </div>
      <div
        class="handling-step-content-element-el flex items-center w-full gap-1 relative"
        :class="{
          'justify-between px-[0.5rem]': props.currentTab === 1,
          'justify-around p-[0]': props.currentTab === 2
        }"
      >
        <div v-if="newService.comment" class="hover-wrap contents">
          <div class="relative">
            <div class="handling-step-tooltip">
              <div>{{ newService.comment }}</div>
            </div>
            <img
              width="44"
              height="44"
              src="../../assets/icons/message-text-square.svg"
              alt="comment"
              class="comment-button cursor-pointer p-[0.75rem] rounded-lg"
              @click="openCommentModal(index)"
            />
          </div>
        </div>
        <img
          v-else
          width="44"
          height="44"
          src="../../assets/icons/message-plus-square.svg"
          alt="comment"
          class="cursor-pointer p-[0.75rem] rounded-lg"
          @click="openCommentModal(index)"
        />
        <Button
          class="button flex items-center button-cancel-service"
          @click="deleteNewService(index)"
        >
          <img
            width="20"
            height="20"
            src="../../assets/icons/cross-red.svg"
            alt="delete"
            class="cursor-pointer"
          />
        </Button>
        <Button
          class="button flex items-center"
          :disabled="isUpdating || !isValidService(newService)"
          @click="onAddService(index)"
          >Save</Button
        >
      </div>
    </div>
  </div>
  <div
    class="handling-step-add-service flex cursor-pointer p-[0.75rem] gap-2 w-fit"
    @click="addNewService"
  >
    <img src="../../assets/icons/plus.svg" alt="add" />
    Add Service to Order
  </div>
  <AddServiceCommentModal
    v-if="modal === 'comment'"
    ref="commentModal"
    :is-open="modal === 'comment'"
    name="new-service-modal"
    :header="
      modalData?.handling_service?.full_repr ?? modalData?.handling_service?.name ?? 'Add Comment'
    "
    :model-value="modalData?.comment ?? ''"
    @modal-submit="onUpdateComment($event, modalIndex)"
    @modal-close="closeModal"
  />
</template>

<script setup lang="ts">
import { computed, type Ref, ref } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { Button } from 'shared/components';
import {
  useMutationAddOrderService,
  useMutationCreateOrderService,
  useMutationDeleteOrderService,
  useMutationUpdateOrderService
} from '@/services/mutations';
import { useQueryHandlingServices } from '@/services/queries';
import CheckboxField from '../forms/fields/CheckboxField.vue';
import InputField from '../forms/fields/InputField.vue';
import SelectField from '../forms/fields/SelectField.vue';
import AddServiceCommentModal from '../modals/AddServiceCommentModal.vue';

import type { IOrder, IOrderNewService, IOrderService } from 'shared/types';

const props = defineProps<{
  order: IOrder;
  currentTab: number;
}>();

const getMockNewService = () => ({
  timestamp: Date.now(),
  id: null,
  name: '',
  comment: '',
  quantity_value: null,
  applies_on_arrival: false,
  applies_on_departure: false,
  is_confirmed: false,
  is_arr_available: true,
  is_dep_available: true,
  is_allowed_quantity_selection: false,
  is_allowed_free_text: false
});

const queryClient = useQueryClient();

const { mutate: updateOrderServiceMutation, isPending: isUpdateOrderServicePending } =
  useMutationUpdateOrderService();

const { mutate: addOrderServiceMutation, isPending: isAddOrderServicePending } =
  useMutationAddOrderService();

const { mutate: createServiceMutation, isPending: isCreateServicePending } =
  useMutationCreateOrderService();

const { isPending: isDeleteServicePending } = useMutationDeleteOrderService();

const orderId = computed(() => props.order?.id);

const newServices: Ref<Array<any>> = ref([]);
const userService = ref([getMockNewService()]);
const displayServices = computed(() => [...userService.value, ...(handlingServices.value ?? [])]);
const modal = ref<'comment' | null>(null);
const modalIndex = ref<number | null>(null);
const modalData = ref<any>(null);
const enabled = computed(() => props.order && props.order.type.is_gh);
const isUpdating = computed(
  () =>
    isAddOrderServicePending.value ||
    isCreateServicePending.value ||
    isUpdateOrderServicePending.value ||
    isDeleteServicePending.value
);

const { data: handlingServices } = useQueryHandlingServices(orderId, { enabled });

const openCommentModal = (index: number) => {
  modal.value = 'comment';
  modalIndex.value = index;
  modalData.value = newServices.value[index];
};

const deleteNewService = (index: number) => {
  newServices.value.splice(index, 1);
};

const onSelectNewService = (value: any, index: number) => {
  newServices.value![index] = { ...value };
};

const handleServiceSearch = (searchTerm: string) => {
  userService.value = [
    {
      ...getMockNewService(),
      name: searchTerm
    }
  ];
};

const closeModal = () => {
  modal.value = null;
  modalData.value = null;
};

const onUpdateComment = (value: string, index: number | null) => {
  if (index === null) return;
  newServices.value[index].comment = value;
};

const onAddService = async (serviceId: number) => {
  const service = newServices.value[serviceId];
  if (service.id) {
    const payload: any = {
      handling_service: service.id,
      applies_on_arrival: service.applies_on_arrival,
      applies_on_departure: service.applies_on_departure,
      quantity_value: service.quantity_value,
      comment: service.comment
    };
    await addOrderServiceMutation(
      {
        orderId: orderId.value!,
        payload
      },
      {
        onSuccess: () => {
          newServices.value!.splice(serviceId, 1);
          queryClient.invalidateQueries({ queryKey: ['orderServices', orderId.value] });
          queryClient.invalidateQueries({ queryKey: ['supplierOrderServices', orderId.value] });
        }
      }
    );
  } else {
    const payload: any = {
      name: service?.name
    };
    await createServiceMutation(
      {
        orderId: orderId.value!,
        payload
      },
      {
        onSuccess: async (newService: IOrderService) => {
          service.id = newService?.id;
          await onUpdateNewService(service, serviceId);
        }
      }
    );
  }
};

const isValidService = (newService: IOrderNewService) => {
  if (
    (newService.is_arr_available || newService.is_dep_available) &&
    !newService.applies_on_arrival &&
    !newService.applies_on_departure
  ) {
    return false;
  }
  return true;
};

const onUpdateNewService = async (service: IOrderService, serviceId: number) => {
  const payload: any = {
    applies_on_arrival: service.applies_on_arrival,
    applies_on_departure: service.applies_on_departure,
    quantity_value: service.quantity_value,
    comment: service.comment
  };
  await updateOrderServiceMutation(
    {
      orderId: orderId.value!,
      handlingServiceId: service.id!,
      payload
    },
    {
      onSuccess: () => {
        newServices.value.splice(serviceId, 1);
        queryClient.invalidateQueries({ queryKey: ['orderServices', orderId.value] });
        queryClient.invalidateQueries({ queryKey: ['supplierOrderServices', orderId.value] });
      }
    }
  );
};

const addNewService = async () => {
  if (newServices.value.length > 0 && isValidService(newServices.value[0])) {
    await onAddService(0);
    newServices.value.push(getMockNewService());
  }
  if (newServices.value.length === 0) {
    newServices.value.push(getMockNewService());
  }
};
</script>
