<template>
  <div class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>移动 {{ targetNode.name }}</h2>
      <select v-model="selectedParentId">
        <option v-for="node in parentNodes" :key="node.id" :value="node.id">{{ node.name }}</option>
      </select>
      <button @click="confirmMove">确认移动</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  targetNode: {
    type: Object,
    default: () => ({})
  }
});

const emits = defineEmits(['close', 'move']);

const selectedParentId = ref(null);

const parentNodes = computed(() => {
  return props.nodes.filter(node => node.type === 'folder' && !node.is_deleted && node.id!== props.targetNode.id);
});

const confirmMove = () => {
  if (selectedParentId.value) {
    emits('move', selectedParentId.value);
  }
};

const closeModal = () => {
  emits('close');
};
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>