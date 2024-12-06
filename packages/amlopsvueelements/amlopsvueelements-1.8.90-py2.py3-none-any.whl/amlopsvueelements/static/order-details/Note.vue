<template>
  <div class="note border-0 rounded-lg">
    <div v-if="isPinned || props?.note?.is_pinned" class="note-header-pinned px-[1rem]">
      <img src="../../assets/icons/pin-02.svg" alt="yes" width="14" height="14" />
      <span>Pinned Note</span>
    </div>
    <div class="pt-[0.75rem] px-[1rem] pb-[1rem] flex flex-col gap-[10px]">
      <div class="note-header">
        <div class="note-header-info flex gap-2 pb-2">
          <Avatar :first-name="firstName" :last-name="lastName" />
          <div class="note-header-info-wrap">
            <div class="note-header-info-name">{{ fullName }}</div>
            <div v-if="props.note?.created_at" class="note-header-info-date">
              {{ toNoteTime(props.note?.created_at) }}
            </div>
          </div>
          <div class="note-header-actions ml-auto flex items-center">
            <div v-if="isNew">
              <button v-if="!isPinned" class="button-pin" @click="togglePin()">
                <img src="../../assets/icons/pin-02.svg" alt="yes" width="14" height="14" />
              </button>
            </div>
            <div v-else-if="isPendingPinNote || isPendingDeleteNote">
              <Loading />
            </div>
            <div v-else>
              <ButtonPopover :left="true" popup-class="top-[2rem] p-0">
                <template #default>
                  <img
                    class="cursor-pointer"
                    src="../../assets/icons/dots-horizontal.svg"
                    alt="More"
                  />
                </template>
                <template #popup>
                  <div class="send-via-email-popup flex flex-col gap-2 cursor-pointer">
                    <div
                      class="el flex gap-2 p-[0.5rem] hover:bg-dark-background"
                      @click="onPin(!!note?.is_pinned)"
                    >
                      {{ note?.is_pinned ? 'Unpin' : 'Pin' }}
                    </div>
                    <div
                      v-if="note?.is_deletable"
                      class="el flex gap-2 p-[0.5rem] hover:bg-dark-background"
                      @click="onClickDelete()"
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
      <p v-if="!isNew" class="note-content flex whitespace-pre-line">
        {{ `${props.note?.content}` }}
      </p>
      <div v-else>
        <TextareaField
          v-model="noteContent"
          placeholder="Leave your note"
          :autofocus="true"
          :is-transparent="true"
        />
        <div v-if="!isPending" class="flex gap-[0.75rem]">
          <Button
            class="button button-green flex items-center gap-2"
            :disabled="!noteContent || isPending"
            @click="onSave()"
            >Save</Button
          >
          <Button
            class="button button-grey flex items-center gap-2"
            @click="emit('closeAddingNote')"
            >Cancel
          </Button>
        </div>
        <div v-else>
          <Loading />
        </div>
      </div>
    </div>
    <ConfirmationModal
      :is-open="modal === 'delete'"
      title="Are you sure you want to delete this note?"
      subtitle="This action cannot be undone."
      cancel-button="No"
      confirm-button="Yes"
      @modal-confirm="onDelete"
      @modal-close="closeModal"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, shallowRef } from 'vue';
import { useQueryClient } from '@tanstack/vue-query';
import { Button } from 'shared/components';
import { useMutationAddOrderNote } from '@/services/mutations';
import { useMutationDeleteNote, useMutationPinNote } from '@/services/mutations';
import { toNoteTime } from '@/helpers/order';
import Avatar from '../forms/Avatar.vue';
import ButtonPopover from '../forms/ButtonPopover.vue';
import TextareaField from '../forms/fields/TextareaField.vue';
import Loading from '../forms/Loading.vue';
import ConfirmationModal from '../modals/ConfirmationModal.vue';

import type { IOrderNote, IUser } from 'shared/types';

type Props = {
  orderId: number;
  note?: IOrderNote;
  currentUser?: IUser;
};

type Emits = {
  (e: 'closeAddingNote'): void;
};

const props = defineProps<Props>();
const emit = defineEmits<Emits>();

const queryClient = useQueryClient();

const isNew = computed(() => !props.note);
const firstName = computed(() =>
  isNew.value && props.currentUser
    ? props.currentUser.details.first_name
    : props.note?.created_by?.details?.first_name
);
const lastName = computed(() =>
  isNew.value && props.currentUser
    ? props.currentUser.details.last_name
    : props.note?.created_by?.details?.last_name
);
const fullName = computed(() => `${firstName.value ?? ''} ${lastName.value ?? ''}`);

const noteContent = shallowRef('');
const isPinned = shallowRef(false);
const modal = shallowRef<'delete' | null>(null);

const { mutate: addOrderNoteMutation, isPending } = useMutationAddOrderNote();
const { mutate: deleteNoteMutation, isPending: isPendingDeleteNote } = useMutationDeleteNote();
const { mutate: pinNoteMutation, isPending: isPendingPinNote } = useMutationPinNote();

const togglePin = () => {
  isPinned.value = !isPinned.value;
};

const onSave = async () => {
  await addOrderNoteMutation(
    {
      orderId: props.orderId,
      payload: {
        content: noteContent.value,
        is_pinned: isPinned.value
      }
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['notes', props.orderId] });
        emit('closeAddingNote');
      }
    }
  );
};

const mutationOptions = {
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['notes', props.orderId] });
  }
};

const onPin = async (unpin?: boolean) => {
  if (!props.note) return;
  await pinNoteMutation(
    {
      orderId: props.orderId,
      noteId: props.note?.id,
      unpin
    },
    mutationOptions
  );
};

const onClickDelete = () => {
  modal.value = 'delete';
};

const closeModal = () => {
  modal.value = null;
};

const onDelete = async () => {
  closeModal();
  if (!props.note) return;
  await deleteNoteMutation(
    {
      orderId: props.orderId,
      noteId: props.note?.id
    },
    mutationOptions
  );
};
</script>

<style scoped lang="scss">
.note {
  background-color: rgba(255, 161, 0, 0.1);

  .note-header {
    &-pinned {
      display: flex;
      align-items: center;
      gap: 6px;
      font-family: 'Inter';
      font-size: 12px;
      font-weight: 500;
      line-height: 16px;
      color: #b87e1a;
      background-color: rgba(255, 161, 0, 0.1);
      min-height: 28px;
      max-height: 28px;
    }

    &-info {
      &-name {
        font-size: 14px;
        font-weight: 600;
        color: rgba(39, 44, 63, 1);
      }

      &-date {
        font-size: 12px;
        font-weight: 400;
        color: rgba(82, 90, 122, 1);
      }
    }
  }

  .note-content {
    font-size: 15px;
    font-weight: 400;
    color: rgba(39, 44, 63, 1);
  }

  .button-pin {
    color: #b87e1a;
    svg {
      color: #b87e1a;
      fill: #b87e1a;
      stroke: #b87e1a;
    }
  }
}
</style>
