<template>
  <Multiselect
    ref="multiselectRef"
    v-bind="$attrs"
    :append-to-body="appendToBody"
    :class="[
      $style['ops-form-select'],
      { 'ops-form-select__error': hasErrors },
      { 'ops-form-select__position-top': position === 'top' },
      { 'ops-form-select__hide-values': hideValues }
    ]"
  >
    <template v-for="(_, name) in $slots" #[name]="slotData">
      <slot :name="name" v-bind="{ slotData }" />
    </template>
  </Multiselect>
</template>

<script lang="ts" setup>
// @ts-ignore
import { ref } from 'vue';
import Multiselect from 'vue-multiselect';
import 'vue-select/dist/vue-select.css';

defineProps({
  hasErrors: {
    type: Boolean,
    default: false
  },
  hideValues: {
    type: Boolean,
    default: false
  },
  position: {
    type: String,
    default: ''
  },
  appendToBody: {
    type: Boolean,
    default: true
  },
  hasIndicator: {
    type: Boolean,
    default: false
  }
});

const multiselectRef = ref(null);
const deactivate = () => {
  if (multiselectRef.value) {
    (multiselectRef.value as any).deactivate();
  }
};
defineExpose({ deactivate });
</script>
<style lang="scss" module scoped>
.ops-form-select {
  background: #eff1f6;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  border: 1px solid transparent;
  border-radius: 0.5rem;

  &__arrow-wrapper {
    @apply absolute cursor-pointer h-full;
  }

  &__arrow {
    @apply border-solid mt-[-2px] cursor-pointer ml-[-4px] absolute w-0 top-1/2 left-1/2 h-0;
    border-color: #888 transparent transparent transparent;
    border-width: 5px 4px 0 4px;
  }

  &__indicator {
    border-radius: 0.5rem 0 0 0.5rem !important;
  }

  @apply w-full cursor-pointer;
}
</style>
<style lang="scss">
.ops-form-select__no_indicator {
  border-radius: 0.5rem;
}

.ops-form-select__indicator {
  border-radius: 0.5rem 0 0 0.5rem !important;
}

.multiselect {
  &--disabled {
    background: var(--vs-disabled-bg) !important;
    cursor: text !important;

    .multiselect__input {
      background: var(--vs-disabled-bg) !important;
    }
  }

  &__placeholder {
    @apply pl-5 text-base text-grey-200 font-light #{!important};
  }

  &__input {
    @apply pl-4 text-grey-950 #{!important};
    background: #eff1f6;

    &::placeholder {
      @apply pl-0 text-base text-grey-200 font-light #{!important};
    }

    &:focus {
      border: 1px solid transparent !important;
      outline: none !important;
    }
  }

  &__content-wrapper {
    position: absolute !important;
    z-index: 1000 !important;
    overflow-y: auto;
    @apply rounded-[0.5rem] max-h-[15rem] border-transparent py-0 mt-4 border-solid text-base text-grey-900 font-normal #{!important};
    -webkit-box-shadow: 0 3px 13px rgba(0, 0, 0, 0.08);
    box-shadow: 0 3px 13px rgba(0, 0, 0, 0.08);
    background: white !important;
    width: 100%;
  }

  &__content {
    width: 100%;

    li {
      background: white;
      color: rgba(133, 141, 173, 1);
    }
  }

  &__element {
    background: rgba(239, 241, 246, 1) !important;
    color: rgba(133, 141, 173, 1) !important;

    &#null-0 {
      padding: 0 !important;
    }
  }

  &__element:not([role='option']) {
    background: rgba(239, 241, 246, 1) !important;
    color: rgba(133, 141, 173, 1) !important;
    @apply pl-4 p-[3px] #{!important};

    &#null-0 {
      padding: 0 !important;
    }
  }

  &__element[role='option'] {
    @apply bg-white font-normal text-[1rem] hover:text-grey-900 overflow-hidden w-full leading-6 font-normal #{!important};

    &:hover {
      background-color: rgba(125, 148, 231, 0.1) !important;
      color: rgb(125, 148, 231) !important;
    }

    .multiselect__option {
      display: flex;
      padding: 6px;
      padding-left: 1rem;
    }
  }

  &__element[role='option']--highlight {
    background-color: rgba(125, 148, 231, 0.1) !important;
    color: rgb(125, 148, 231) !important;
  }

  &__element:has(> .multiselect__option--selected) {
    background-color: rgba(125, 148, 231, 0.1) !important;
    color: rgb(125, 148, 231) !important;
  }

  &__option {
    display: flex;
    gap: 8px;
    &:before {
      content: '☐';
      color: rgb(125, 148, 231);
      font-size: 16px;
      font-style: normal;
    }
  }

  &__option--selected {
    display: flex;
    gap: 8px;

    &:before {
      content: '☑';
      color: rgb(125, 148, 231);
      font-size: 16px;
      font-style: normal;
    }
  }

  &__option--group {
    &:before {
      content: none;
    }
  }

  &__single {
    margin-left: 1rem !important;
    @apply text-grey-950 text-[0.875rem] #{!important};
  }

  &__tags {
    height: 24px;

    input {
      width: 100% !important;
    }
  }

  &__tags-wrap {
    flex-wrap: wrap;
    gap: 4px;
    width: fit-content;
    margin-left: 4px;
  }

  &__tag {
    color: rgba(21, 28, 53, 1) !important;
    font-size: 16px !important;
    font-weight: 400 !important;
    // display: flex;
    display: none;
    background-color: white;
    padding-left: 4px;
    padding-right: 4px;
    border-radius: 4px;

    &-icon {
      display: block;
      margin-right: 4px;
      margin-left: 8px;

      &:after {
        content: '×';
        color: #266d4d;
        font-size: 16px;
        font-style: normal;
      }
    }
  }
}

.ops-form-select__error {
  .vs__dropdown-toggle {
    @apply border-amaranth-900 #{!important};
  }
}
</style>
