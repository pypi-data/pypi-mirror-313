<template>
  <div class="pricing-step bg-white w-full border border-transparent rounded-md">
    <div class="pricing-step-header flex justify-between items-center py-[0.5rem] px-[0.75rem]">
      <div class="pricing-step-header-name">CRM Activity</div>
      <div class="pricing-step-header-actions flex gap-4">
        <img
          width="20"
          height="20"
          src="../../assets/icons/filter.svg"
          alt="filter"
          class="cursor-pointer"
        />
        <Button
          v-if="userStore.hasCRMPermission"
          class="button flex items-center gap-2"
          @click="openAddModal"
        >
          <img src="../../assets/icons/plus.svg" alt="add" />
          Add Activity
        </Button>
      </div>
    </div>
    <div v-if="isPending || isEmpty" class="pricing-step-content w-full flex flex-col">
      <Loading v-if="isPending" />
      <p
        v-if="isEmpty"
        class="pricing-step-content-missing flex items-center justify-center py-[1.25rem]"
      >
        <span>No activities yet</span>
      </p>
    </div>
    <div v-if="isShown" class="pricing-step-content w-full flex flex-col">
      <div class="pricing-step-content-header-wrap w-full flex items-center">
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Recorded by</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Date & Time</div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Activity Type</div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">
            Applicable person
          </div>
        </div>
        <div class="pricing-step-content-col w-4/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Description</div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-header px-[0.75rem] py-[0.5rem]">Attachments</div>
        </div>
      </div>
      <div
        v-for="(activity, activityIndex) in crmData"
        :key="activityIndex"
        class="pricing-step-content-data-wrap order-crm w-full flex items-center"
      >
        <div class="pricing-step-content-col w-2/12">
          <div
            class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem] flex gap-2 items-center"
          >
            <Avatar
              :first-name="activity.created_by.details.first_name"
              :last-name="activity.created_by.details.last_name"
              :is-small="true"
            />
            {{ activity.created_by.details.full_name }}
          </div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ toUTCdateTime(activity.datetime) }}
          </div>
        </div>
        <div class="pricing-step-content-col w-1/12">
          <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ activity.activity_type.name }}
          </div>
        </div>
        <div class="pricing-step-content-col w-2/12">
          <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ activity.person ?? '--' }}
          </div>
        </div>
        <div class="pricing-step-content-col w-4/12">
          <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
            {{ activity.description }}
          </div>
        </div>
        <div class="pricing-step-content-col w-10pc">
          <div class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem]">
            <div
              v-if="activity.attachments.length > 0"
              class="files-button flex gap-2 justify-center cursor-pointer"
            >
              <img width="12" height="12" src="../../assets/icons/paperclip.svg" alt="file" />
              {{ activity.attachments.length }}
              {{ activity.attachments.length === 1 ? 'file' : 'files' }}
            </div>
            <div v-else>--</div>
          </div>
        </div>
        <div class="pricing-step-content-col w-6pc">
          <div v-if="isPendingDelete">
            <Loading />
          </div>
          <div
            v-else-if="userStore.hasCRMPermission"
            class="pricing-step-content-col-data px-[0.75rem] py-[0.5rem] flex justify-center"
          >
            <ButtonPopover :left="true" popup-class="bottom-[2rem] top-auto p-0">
              <template #default>
                <img
                  width="20"
                  height="20"
                  src="../../assets/icons/dots-vertical.svg"
                  alt="options"
                  class="horizontal cursor-pointer"
                />
              </template>
              <template #popup>
                <div class="send-via-email-popup flex flex-col gap-2 cursor-pointer">
                  <div
                    class="el flex gap-2 p-[0.5rem] hover:bg-dark-background"
                    @click="onEdit(activity)"
                  >
                    Edit
                  </div>
                  <div
                    class="el flex gap-2 p-[0.5rem] hover:bg-dark-background"
                    @click="onClickDelete(activity.id)"
                  >
                    Delete
                  </div>
                </div>
              </template>
            </ButtonPopover>
          </div>
        </div>
      </div>
    </div>
    <AddCRMActivityModal
      v-if="modal === 'add' || modal === 'edit'"
      :is-open="true"
      :activity="editActivity"
      :order-id="orderId"
      @modal-close="closeModal"
    />
    <ConfirmationModal
      v-if="modal === 'delete' && modalData"
      :is-open="modal === 'delete'"
      header="Delete CRM Activity"
      title="Are you sure you want to delete this CRM Activity?"
      @modal-close="closeModal"
      @modal-confirm="onDelete(modalData)"
    />
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, shallowRef } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { onKeyStroke } from '@vueuse/core';
import { Button } from 'shared/components';
import { useOrderStore } from '@/stores/useOrderStore';
import { useUserStore } from '@/stores/useUserStore';
import { useMutationDeleteCRMActivity } from '@/services/mutations/crm-activity';
import { useQueryCRMActivity } from '@/services/queries';
import { toUTCdateTime } from '@/helpers/order';
import Avatar from '../forms/Avatar.vue';
import ButtonPopover from '../forms/ButtonPopover.vue';
import Loading from '../forms/Loading.vue';
import AddCRMActivityModal from '../modals/AddCRMActivityModal.vue';
import ConfirmationModal from '../modals/ConfirmationModal.vue';

import type { ICrmActivity } from 'shared/types';

const orderStore = useOrderStore();
const userStore = useUserStore();
const queryClient = useQueryClient();

const orderId = computed(() => orderStore.orderId);

const { data: crmData, isPending, isSuccess } = useQueryCRMActivity(orderId);
const { mutate: deleteCRMActivity, isPending: isPendingDelete } = useMutationDeleteCRMActivity();

const modal = shallowRef<'add' | 'edit' | 'delete' | null>(null);
const modalData = ref<number | null>(null);
const editActivity = ref<ICrmActivity | null>(null);
const isEmpty = computed(() => isSuccess && crmData.value?.length === 0);
const isShown = computed(() => isSuccess && !!crmData.value?.length);

const openAddModal = () => (modal.value = 'add');

const closeModal = () => {
  modal.value = null;
  editActivity.value = null;
};

const onEdit = (activity: ICrmActivity) => {
  modal.value = 'edit';
  editActivity.value = activity;
};

const onClickDelete = (activityId: number) => {
  modal.value = 'delete';
  modalData.value = activityId;
};

const onDelete = async (activityId: number) => {
  closeModal();
  await deleteCRMActivity(
    { activityId, orderId: orderId.value },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['CRMActivity', orderId.value] });
      }
    }
  );
};

onKeyStroke('Escape', closeModal);
</script>

<style lang="scss">
.button {
  background-color: rgba(81, 93, 138, 1) !important;
  color: white !important;
  font-weight: 500 !important;
  font-size: 16px !important;
  @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-lg #{!important};
}

.order-crm {
  background-color: rgb(255, 255, 255) !important;
  .pricing-step-content-col-data {
    color: rgba(39, 44, 63, 1);
  }
}

.w-10pc {
  width: 10%;
}
.w-6pc {
  width: 6.66666%;
}
</style>
