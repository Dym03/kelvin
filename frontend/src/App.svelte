<script>
import EditTask from './EditTask.svelte';
import ClassList from './ClassList.svelte';
import Router from 'svelte-spa-router';
import StudentTransfer from './StudentTransfer.svelte';
import { user } from './global.js';

const routes = {
  '/task/edit/:id': EditTask,
  '/task/add/:subject': EditTask,
  '/student_transfer': StudentTransfer,
  '/': ClassList
};
</script>

{#if $user}
  <Router {routes} />
{/if}
