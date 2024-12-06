<template>
  <div :class="[{ 'ops-input-wrapper': true }, props.class]">
    <Label v-if="labelText" :required="required" :label-text="labelText" />
    <div
      class="u-input-wrapper"
      :class="[
        'ops-input',
        {
          'ops-input__focus': isFocused,
          'ops-input__disabled': disabled,
          'ops-input__white': isWhite,
          'ops-input__transparent': isTransparent,
          'ops-input__error': hasErrors && isValidationDirty && !disabled
        }
      ]"
    >
      <slot name="prefix" />
      <textarea
        v-bind="$attrs"
        ref="textarea"
        :class="'ops-input__input'"
        :value="formattedInputNumber"
        :type="type"
        :min="type === 'number' ? 0 : undefined"
        :placeholder="placeholder"
        :disabled="disabled"
        @focus="toggleFocus(true)"
        @blur="toggleFocus(false)"
        @input="onInput"
        @keydown="(e) => emits('keydown', e)"
      />
      <slot name="suffix" />
    </div>
    <p v-if="typeof errors === 'string' && !disabled" :class="'ops-input-text__error'">
      <span>{{ errors }}</span>
    </p>
    <p v-else-if="hasErrors && isValidationDirty && !disabled" :class="'ops-input-text__error'">
      <span v-for="(error, index) in errors" :key="`${index}_${(error as ErrorObject).$property}`">
        {{ index === 0 ? (error as ErrorObject).$message : '' }}
      </span>
    </p>
  </div>
</template>

<script lang="ts" setup>
import { computed, onMounted, type PropType, ref } from 'vue';
// @ts-ignore
import type { ErrorObject } from '@vuelidate/core';
import { Label } from 'shared/components';

const props = defineProps({
  labelText: {
    type: String,
    default: ''
  },
  class: {
    type: String,
    default: ''
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  type: {
    type: String,
    default: 'text'
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  placeholder: {
    type: String,
    default: 'Enter a value'
  },
  isTransparent: {
    type: Boolean,
    default: false
  },
  isWhite: {
    type: Boolean,
    default: false
  },
  autofocus: {
    type: Boolean,
    default: false
  },
  errors: {
    type: [Array, String] as PropType<ErrorObject[] | string>,
    default: () => []
  },
  modelModifiers: {
    type: Object,
    default: () => ({})
  }
});
const emits = defineEmits(['update:modelValue', 'keydown']);

const textarea = ref<null | HTMLTextAreaElement>(null);

onMounted(() => {
  props.autofocus && textarea?.value?.focus();
});

const formattedInputNumber = computed(() => {
  return props.type === 'number' && props.modelValue ? Number(props.modelValue) : props.modelValue;
});

const hasErrors = computed(() => {
  return !!props.errors?.length || typeof props.errors === 'string';
});

const isFocused = ref<boolean>(false);
const toggleFocus = (flag: boolean) => (isFocused.value = flag);

const onInput = (event: Event) => {
  const inputElement = event?.target as HTMLInputElement | null;

  if (inputElement) {
    let inputValue = inputElement.value;
    if (props.modelModifiers.uppercase) {
      inputValue = inputValue.toUpperCase();
    }
    emits('update:modelValue', inputValue);
  }
};
</script>

<style lang="scss">
.ops-input {
  @apply flex items-center appearance-none text-[0.875rem] bg-clip-padding leading-6 font-normal focus:outline-none text-grey-700 w-full border-transparent border-[0.0625rem] border-solid rounded-[0.5rem] py-[0.5rem] px-[1rem] pl-[0.6875rem] pl-[1.0625rem];
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07);
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  background: #eff1f6;

  &-text__error {
    @apply text-amaranth-900 -bottom-8 lg:-bottom-4 text-xs;
  }

  &:has(&__input:disabled) {
    @apply bg-grey-disabled text-grey-400;
  }

  &__error {
    @apply border-red-500 #{!important};
  }

  &__icon {
    @apply h-4 w-4 opacity-50 mr-2;
  }

  &__input {
    @apply w-full text-grey-950 text-[0.875rem] font-medium py-0 px-0 border-0 outline-none #{!important};
    background: #eff1f6 !important;

    &::placeholder {
      @apply text-grey-200 text-base font-light #{!important};
    }

    &:disabled {
      @apply bg-grey-disabled text-grey-400;
    }
  }

  &__white {
    background: #fff !important;
    border: 1px solid rgba(223, 226, 236, 1) !important;

    .ops-input__input {
      background: #fff !important;
      font-size: 13px !important;
      color: rgba(21, 28, 53, 1) !important;
    }
  }

  &__transparent {
    background: transparent !important;
    /* border: none !important; */

    .ops-input__input {
      background: transparent !important;
      font-size: 15px !important;
      color: theme('colors.base.800') !important;
      line-height: 24px !important;
    }
  }

  &__focus {
    @apply border-grey-300 text-grey-700 outline-0;
    box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.07), 0 0 0 0.18rem rgba(81, 93, 138, 0.25);
  }

  &-wrapper {
    @apply relative w-full flex flex-col break-words items-start justify-start rounded-[0.5rem] mb-4;

    &-white {
      background: #fff !important;
    }
  }
}
</style>
