package com.nameproject.nameproject5At.pythonConnect;
//
//import com.nameproject.nameproject5At.NameProjectApplication;
//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;
//import py4j.GatewayServer;
//
///*
// * 说一下怎么个事。
// * 我本来打算使用JNativeHook进行全局键盘监听操作的。
// * 但是这个库是一个非模块化的，项目不能被jlink打包。
// * 于是当时懵懂的我开始寻找替代
// */
//public class PythonConnecter {
//    private static final Logger logger = LogManager.getLogger(PythonConnecter.class);
//
//    public void sayHello() {
//        System.out.println("Hello from Java!");
//    }
//
//    public void PythonAndJavaConnectionTester() {
//        System.out.println("Testing connection from Python to Java");
//    }
//
//    public static void initMethod() {
//        // Java 与 Python 的通讯模块加载
//        GatewayServer gatewayServer = new GatewayServer(new NameProjectApplication(), 57350);
//        gatewayServer.start();
//        logger.info("GatewayServer started on port 57350");
//    }
//}
