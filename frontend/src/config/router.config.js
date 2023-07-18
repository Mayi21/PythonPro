export const asyncRouterMap = [
    {
        path: "/",
        name: "index",
        component: BasicLayout,
        meta: { title: "menu.home" },
        redirect: "/helloworld",
        children: [
            // helloworld
            {
                path: "/helloworld",
                name: "hello-world",
                component: HelloWorld,
                meta: {
                    title: "menu.hello",
                    icon: "folder",
                    permission: ["dashboard"],
                },
            },
        ],
    },
    {
        path: "*",
        redirect: "/404",
        hidden: true,
    },
];