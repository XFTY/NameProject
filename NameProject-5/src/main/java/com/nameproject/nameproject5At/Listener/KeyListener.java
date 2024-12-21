package com.nameproject.nameproject5At.Listener;

import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.keyboard.NativeKeyEvent;
import org.jnativehook.keyboard.NativeKeyListener;

public class KeyListener implements NativeKeyListener {

    public KeyListener() {
        java.util.logging.LogManager.getLogManager().reset();

        System.out.println("KeyListener initialized");

        // 注册全局键盘监听器
        try {
            GlobalScreen.registerNativeHook();
            System.out.println("GlobalScreen native hook registered successfully.");
        } catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            ex.printStackTrace();
        }

        // 添加键盘事件监听器
        GlobalScreen.addNativeKeyListener(this);
        System.out.println("NativeKeyListener added successfully.");
    }

    @Override
    public void nativeKeyTyped(NativeKeyEvent nativeKeyEvent) {
        // 检查是否按下反引号键
        if (nativeKeyEvent.getKeyCode() == NativeKeyEvent.VC_BACKQUOTE) {
            System.out.println("反引号键被按下");
        }
    }

    @Override
    public void nativeKeyPressed(NativeKeyEvent nativeKeyEvent) {
//        System.out.println("Key pressed: " + nativeKeyEvent.getKeyText(nativeKeyEvent.getKeyCode()));
        if (nativeKeyEvent.getKeyCode() == NativeKeyEvent.VC_BACKQUOTE) {
            System.out.println("反引号键被按下");
        }
    }

    @Override
    public void nativeKeyReleased(NativeKeyEvent nativeKeyEvent) {
//        System.out.println("Key released: " + nativeKeyEvent.getKeyText(nativeKeyEvent.getKeyCode()));
    }

//    public static void main(String[] args) {
//        new KeyListener();
//    }
}
