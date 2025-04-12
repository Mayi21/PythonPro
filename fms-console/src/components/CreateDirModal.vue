<template>
  <div class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>创建目录</h2>
      <input type="text" v-model="dirName" placeholder="目录名" />
      <select v-model="selectedParentId">
        <option v-for="node in parentNodes" :key="node.id" :value="node.id">{{ node.name }}</option>
      </select>
      <button @click="createDir">创建</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { defineEmits } from 'vue';

const emits = defineEmits(['close', 'create']);

const dirName = ref('');
const selectedParentId = ref(null);
const parentNodes = ref([]);

const fetchParentNodes = async () => {
  try {
    const response = await axios.get('/api/nodes');
    parentNodes.value = response.data.filter(node => node.type === 'folder' && !node.is_deleted);
  } catch (error) {
    console.error('获取父节点信息失败:', error);
  }
};

const createDir = () => {
  if (dirName.value && selectedParentId.value) {
    emits('create', dirName.value, selectedParentId.value);
  }
};

const closeModal = () => {
  emits('close');
};

onMounted(fetchParentNodes);
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