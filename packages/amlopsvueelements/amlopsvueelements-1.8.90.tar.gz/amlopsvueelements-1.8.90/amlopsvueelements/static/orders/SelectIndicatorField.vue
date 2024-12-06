<template>
  <div
    :class="[
      $style['ops-select-wrapper'],
      { 'flex items-center flex-row': isHorizontalWrapper, 'max-w-64': smallWidth }
    ]"
  >
    <Label v-if="!multiple && labelText" :required="required" :label-text="labelText" />
    <div class="flex w-full">
      <Select
        v-model="computedValue"
        :placeholder="placeholder"
        :has-errors="hasErrors && isValidationDirty && !disabled"
        v-bind="$attrs"
        :append-to-body="appendToBody"
        :has-indicator="true"
        :position="position"
        :taggable="taggable"
        :hide-values="hideValues"
        :multiple="multiple"
        :disabled="disabled"
      >
        <template #select-option="item">
          <slot name="select-option" v-bind="item" />
        </template>
        <template v-for="(_, name) in $slots" #[name]="slotData">
          <slot :name="name" v-bind="slotData" />
        </template>
      </Select>
      <div
        class="w-3/12 flex items-center justify-center ops-select__indicator"
        :class="{
          'indicator-error': hasErrors || !computedValue,
          'indicator-value': indicatorValue
        }"
        :style="getStyles()"
      >
        {{
          indicatorValue
            ? indicatorValue
            : indicatorValueObj
            ? indicatorValueObj.name
            : !computedValue
            ? indicatorDisplay
            : 'No List'
        }}
      </div>
    </div>

    <p v-if="typeof errors === 'string' && !disabled" :class="$style['ops-select__error']">
      <span>{{ errors }}</span>
    </p>
    <p v-else-if="hasErrors && isValidationDirty && !disabled" :class="$style['ops-select__error']">
      <span v-for="(error, index) in errors" :key="`${index}_${(error as ErrorObject).$property}`">
        {{ index === 0 ? (error as ErrorObject).$message : '' }}
      </span>
    </p>
  </div>
</template>

<script lang="ts" setup>
import { computed, type PropType } from 'vue';
// @ts-ignore
import type { ErrorObject } from '@vuelidate/core';
import { Label } from 'shared/components';
import Select from '../Select.vue';

const props = defineProps({
  labelText: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  hideValues: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  taggable: {
    type: Boolean,
    default: false
  },
  isHorizontalWrapper: {
    type: Boolean,
    default: false
  },
  modelValue: {
    type: [String, Number, Boolean, Object, null] as PropType<
      string | number | boolean | object | null
    >,
    default: () => null
  },
  multiple: {
    type: Boolean,
    default: false
  },
  errors: {
    type: [Array, String] as PropType<ErrorObject[] | string>,
    default: () => []
  },
  isValidationDirty: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an option'
  },
  appendToBody: {
    type: Boolean,
    default: true
  },
  smallWidth: {
    type: Boolean,
    default: false
  },
  indicatorDisplay: {
    type: String,
    default: 'Choose value'
  },
  indicatorValue: {
    type: String,
    default: ''
  },
  indicatorValueObj: {
    type: Object,
    default: null
  }
});
const emit = defineEmits<{
  (e: 'update:modelValue', v: any): void;
}>();

const hasErrors = computed(() => {
  return !!props.errors?.length || typeof props.errors === 'string';
});

const getStyles = () => {
  if (props.indicatorValueObj) {
    return {
      'background-color': props.indicatorValueObj.fill_colour_hex,
      color: props.indicatorValueObj.text_colour_hex
    };
  }
  return {};
};

const computedValue = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    return emit('update:modelValue', value);
  }
});
</script>
<style lang="scss" module>
.ops-select-wrapper {
  @apply relative w-full flex flex-col break-words items-start justify-start mb-4;
}

.ops-select-wrapper__error {
  @apply border border-red-800 #{!important};
}

.ops-select__error {
  @apply text-amaranth-900 text-xs;
  position: absolute !important;
  bottom: -1rem !important;
}
</style>

<style lang="scss">
.ops-select__indicator {
  background-color: #fafbff;
  color: rgba(191, 197, 217, 1);
  font-size: 14px;
  border-radius: 0 0.5rem 0.5rem 0;
}
.indicator-error {
  background-color: #fafbff !important;
  color: rgba(191, 197, 217, 1) !important;
}

.indicator-value {
  background-color: rgba(98, 132, 254, 0.12) !important;
  color: rgb(98, 132, 254) !important;
}
</style>
