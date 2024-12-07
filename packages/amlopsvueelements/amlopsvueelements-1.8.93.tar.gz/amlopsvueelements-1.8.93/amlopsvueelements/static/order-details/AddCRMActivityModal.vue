<template>
  <div v-if="isOpen" class="order-modal add-activity-modal">
    <div class="order-modal-wrapper">
      <div class="order-modal-container">
        <div class="order-modal-body">
          <OrderForm is-modal>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">{{ headerTitle }}</div>
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
              <ScrollBar>
                <div class="form-body-wrapper px-[1.5rem] py-[0.5rem]">
                  <TextareaField
                    v-model="description"
                    class="w-full"
                    label-text="Description"
                    :required="true"
                    placeholder="Add activity description"
                  />
                  <Label :required="true" label-text="Datetime" />
                  <div class="flex items-center gap-[1rem] mt-[0.25rem] mb-[0.75rem] w-full">
                    <FlatPickr
                      v-model="fromDateTime.date"
                      :config="{
                        allowInput: true,
                        altInput: true,
                        altFormat: 'Y-m-d',
                        dateFormat: 'Y-m-d'
                      }"
                    />
                    <FlatPickr
                      v-model="fromDateTime.time"
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
                    />
                  </div>
                  <div class="mt-[0.25rem] mb-[0.75rem] w-full">
                    <Loading v-if="isTypesPending" />
                    <SelectField
                      v-else
                      v-model="activityType"
                      label-text="Activity Type"
                      :required="true"
                      class="w-6/12"
                      placeholder=""
                      label="description_plural"
                      :options="activityTypeOptions"
                    ></SelectField>
                  </div>
                  <div class="w-full pb-[0.75rem]">
                    <Attachments
                      :initial-attachments="activity?.attachments"
                      @on-change="onChangeAttachments"
                      @on-delete="onDeleteAttachment"
                    />
                  </div>
                </div>
              </ScrollBar>
            </template>
          </OrderForm>
        </div>
        <div class="order-modal-footer">
          <Loading v-if="isPending" class="mr-1" />
          <button class="modal-button h-[44px] cancel" @click.stop="emit('modal-close')">
            Close
          </button>
          <button :disabled="isPending" class="modal-button h-[44px] submit" @click.stop="onSave()">
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref, shallowRef } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import OrderForm from '@/components/forms/OrderForm.vue';
import {
  useMutationAddCRMActivity,
  useMutationAddCRMActivityAttachment,
  useMutationDeleteCRMActivityAttachment,
  useMutationUpdateCRMActivity,
  useMutationUpdateCRMActivityAttachment
} from '@/services/mutations/crm-activity';
import { useQueryCRMActivityTypes } from '@/services/queries';
import { getAttachmentsToAddUpdate } from '@/helpers/crm-activity';
import { toUTCdateTime } from '@/helpers/order';
import { notify } from '@/helpers/toast';
import FlatPickr from '../FlatPickr/FlatPickr.vue';
import Attachments, { type Attachment, type TableAttachment } from '../forms/Attachments.vue';
import SelectField from '../forms/fields/SelectField.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Label from '../forms/Label.vue';
import Loading from '../forms/Loading.vue';
import ScrollBar from '../forms/ScrollBar.vue';

import type { ICrmActivity } from 'shared/types';

type Props = {
  isOpen: boolean;
  orderId: number;
  activity: ICrmActivity | null;
};

const props = defineProps<Props>();

const emit = defineEmits(['modal-close', 'modal-submit']);

const queryClient = useQueryClient();

const { data: crmActivityTypes, isPending: isTypesPending } = useQueryCRMActivityTypes();
const { mutate: addActivityMutation, isPending: isAddActivityPending } =
  useMutationAddCRMActivity();
const { mutate: updateActivityMutation, isPending: isUpdateActivityPending } =
  useMutationUpdateCRMActivity();
const { mutateAsync: updateActivityAttachmentMutationAsync } =
  useMutationUpdateCRMActivityAttachment();
const { mutateAsync: deleteActivityAttachmentMutationAsync } =
  useMutationDeleteCRMActivityAttachment();
const {
  mutateAsync: addActivityAttachmentMutationAsync,
  isPending: isAddPending,
  status: addStatus
} = useMutationAddCRMActivityAttachment();

const isPendingAsync = shallowRef(false);
const isPending = computed(
  () => isAddActivityPending.value || isUpdateActivityPending.value || isPendingAsync.value
);
const headerTitle = computed(() => (props.activity ? 'Edit CRM Activity' : 'Add CRM Activity'));
const utcDateTime = computed(() =>
  props.activity ? toUTCdateTime(props.activity.datetime).split(' ') : ''
);

const attachments = ref<Attachment[]>([]);
const attachmentIdsToDelete = ref<number[]>([]);
const description = ref(props.activity?.description ?? '');
const activityType = ref<string>(props.activity?.activity_type.name ?? '');
const fromDateTime = ref({
  date: utcDateTime.value ? utcDateTime.value[0] : new Date().toLocaleDateString('en-CA'),
  time: utcDateTime.value ? utcDateTime.value[1] : new Date().getTime().toString()
});
const activityTypeOptions = computed(() => crmActivityTypes.value?.map((type) => type.name) ?? []);

const hasError = (isFileDescriptionMissing: boolean) => {
  let error = '';

  if (isFileDescriptionMissing) error = 'File description is required';
  if (!activityType.value) error = 'Activity Type is required';
  if (!fromDateTime.value.date || !fromDateTime.value.time) error = 'Date and time are required';
  if (!description.value) error = 'Description is required';

  if (error) notify(error, 'error');
  return error;
};

const onChangeAttachments = (nextAttachments: Attachment[]) => {
  attachments.value = nextAttachments;
};

const onSave = async () => {
  const { toAdd, toUpdate } = getAttachmentsToAddUpdate(
    props.activity?.attachments,
    attachments.value
  );

  const isFileDescriptionMissing =
    toAdd.some((attachment) => !attachment.description) ||
    toUpdate.some((attachment) => !attachment.description);

  if (hasError(isFileDescriptionMissing)) return;

  const addCount = toAdd.length;
  const updateCount = toUpdate.length;
  const attachmentsSaveCount = addCount + updateCount + attachmentIdsToDelete.value.length;

  const activityTypeId = crmActivityTypes.value?.find(
    (type) => type.name === activityType.value
  )?.id;

  if (!activityTypeId) {
    notify('Invalid activity type', 'error');
    return;
  }

  const payload = {
    orderId: props.orderId,
    activityId: props.activity?.id ?? 0,
    payload: {
      description: description.value,
      activity_type: activityTypeId,
      datetime: `${fromDateTime.value.date} ${fromDateTime.value.time}`
    }
  };

  const onSuccess = () => {
    queryClient.invalidateQueries({ queryKey: ['CRMActivity', props.orderId] });
    emit('modal-close');
  };

  const isNewActivity = !props.activity;
  const mutationFn = isNewActivity ? addActivityMutation : updateActivityMutation;

  if (!attachmentsSaveCount) {
    await mutationFn(payload, { onSuccess });
  } else {
    await mutationFn(payload, {
      onSuccess: async (data) => {
        try {
          const activityId = data.id;

          isPendingAsync.value = true;

          await Promise.all([
            ...attachmentIdsToDelete.value.map((attachmentId) =>
              deleteActivityAttachmentMutationAsync({
                orderId: props.orderId,
                activityId,
                attachmentId
              })
            ),
            ...toAdd.map((attachment) =>
              addActivityAttachmentMutationAsync({
                orderId: props.orderId,
                activityId,
                payload: { file: attachment.file, description: attachment.description }
              })
            ),
            ...toUpdate.map((attachment) =>
              updateActivityAttachmentMutationAsync({
                orderId: props.orderId,
                activityId,
                attachmentId: attachment.id,
                payload: { description: attachment.description }
              })
            )
          ]);

          onSuccess();
        } catch {
          notify('Error saving attachments', 'error');
        } finally {
          isPendingAsync.value = false;
        }
      }
    });
  }
};

const onDeleteAttachment = (attachment: TableAttachment) => {
  if (typeof attachment.file !== 'string') return;

  attachmentIdsToDelete.value.push(attachment.id);
};
</script>

<style scoped lang="scss">
.add-activity-modal {
  .order-modal-footer {
    align-items: center;
    min-height: 72px;
    max-height: 72px;
  }

  .order-modal-container {
    width: 680px;
  }

  .form-body-wrapper {
    height: calc(80vh - 144px);
    max-height: calc(80vh - 144px);
  }
}
</style>
