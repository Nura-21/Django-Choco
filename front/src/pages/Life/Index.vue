<template>
  <main class="mt-5 max-w-[1060px] mx-auto pb-96">
    <ul class="grid grid-cols-3 gap-5">
      <li 
        v-for="ev in $store.eventsData" 
        :key="ev.title" 
        class="hover:cursor-pointer relative"
        @click="$router.replace({ name: 'chocolifeEvent', params: { id: ev.id, event: JSON.stringify(ev) }})"
      >
        <img :src="ev.img" class="rounded-lg" />
        <p class="absolute max-w-[200px] truncate left-2 top-2 py-1 px-3 bg-[rgba(0,0,0,.3)] rounded-xl text-sm text-white">{{ ev.company.sale_points }}</p>
        <p class="mt-2 truncate leading-[18px]">{{ ev.title }}</p>
        <p class="mt-1 text-xs">{{ ev.company.title }}</p>
      </li>
    </ul>
  </main>
</template>

<script>
  import { useStore } from '@/store';

  export default {
    setup() {
      const store = useStore();

      const initPage = async () => {
        store.isLoading = true;
        store.getCompanies().then(() => store.getLifeCertificates()).then(() => store.getCategoryEvents(0));
        store.isLoading = false;
      }

      initPage();
    }
  }
</script>