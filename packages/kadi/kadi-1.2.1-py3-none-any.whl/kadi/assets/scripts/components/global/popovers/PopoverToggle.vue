<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <span v-trim-ws>
    <a ref="toggle" tabindex="-1" data-toggle="popover" class="cursor-pointer" :class="toggleClass">
      <slot name="toggle"></slot>
    </a>
    <span ref="popoverContent" class="d-none">
      <slot name="content"></slot>
    </span>
    <span ref="popoverTitle" class="d-none">
      <slot name="title">
        <strong v-if="title">{{ title }}</strong>
      </slot>
    </span>
  </span>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: null,
    },
    toggleClass: {
      type: String,
      default: 'btn btn-light',
    },
    width: {
      type: Number,
      default: 450,
    },
    placement: {
      type: String,
      default: 'auto',
    },
    trigger: {
      type: String,
      default: 'focus',
    },
    container: {
      type: String,
      default: 'body',
    },
  },
  mounted() {
    const vm = this;

    $(vm.$refs.toggle).popover({
      container: vm.container,
      placement: vm.placement,
      trigger: vm.trigger,
      html: true,
      title: () => $(vm.$refs.popoverTitle).html(),
      content: () => $(vm.$refs.popoverContent).html(),
    }).on('inserted.bs.popover', function() {
      const width = Math.min(window.innerWidth - 20, vm.width);
      $($(this).data('bs.popover').getTipElement()).css('width', `${width}px`);
    });
  },
  beforeDestroy() {
    $(this.$refs.toggle).popover('dispose');
  },
};
</script>
