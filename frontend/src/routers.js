import {createRouter, createWebHistory} from "vue-router";
import HelloWorld from "@/components/HelloWorld";
import MessageSend from "@/components/MessageSend";

const routes = [
    {
        path: '/',
        name: 'helloWorld',
        component: HelloWorld
    },
    {
        path: '/message',
        name: 'messageSend',
        component: MessageSend
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;
