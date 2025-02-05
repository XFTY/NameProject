/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.Listener;

import com.nameproject.nameproject5At.flusher.Flush2v;

import com.github.kwhat.jnativehook.GlobalScreen;
import com.github.kwhat.jnativehook.NativeHookException;
import com.github.kwhat.jnativehook.keyboard.NativeKeyEvent;
import com.github.kwhat.jnativehook.keyboard.NativeKeyListener;


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
        if (nativeKeyEvent.getKeyCode() == NativeKeyEvent.VC_F6) {
            System.out.println("user pushed keyboard '`' .");
            Flush2v.fastFlush();
        }
    }

    @Override
    public void nativeKeyPressed(NativeKeyEvent nativeKeyEvent) {
//        System.out.println("Key pressed: " + nativeKeyEvent.getKeyText(nativeKeyEvent.getKeyCode()));
        if (nativeKeyEvent.getKeyCode() == NativeKeyEvent.VC_F6) {
            // System.out.println("反引号键被按下");
            System.out.println("user native keyboard '`' .");
            Flush2v.fastFlush();
        }
    }

    @Override
    public void nativeKeyReleased(NativeKeyEvent nativeKeyEvent) {
        if (nativeKeyEvent.getKeyCode() == NativeKeyEvent.VC_F6) {
//            // System.out.println("反引号键被按下");
//            System.out.println("user native keyboard '`' .");
//            Flush2v.fastFlush();
        }
//        System.out.println("Key released: " + nativeKeyEvent.getKeyText(nativeKeyEvent.getKeyCode()));
    }

//    public static void main(String[] args) {
//        new KeyListener();
//    }
}
