/* Copyright 2024-2025 XFTY, All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * For more information, see the LICENSE file in the root directory.
 */
package com.nameproject.nameproject5At.IO;

public class IOManager {
    // 控件变量
    // 用于查看那些线程在修改那些控件，防止线程冲突

    public static boolean isFlushing = false;

    public static boolean IsMiniWindowShowing = false;

    public static boolean ReturnIsMiniWindowShowing() {
        return IsMiniWindowShowing;
    }

    public static void SetIsMiniWindowShowing(boolean isMiniWindowShowing) {
        IsMiniWindowShowing = isMiniWindowShowing;
    }

}
