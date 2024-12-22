from py4j.java_gateway import JavaGateway, GatewayParameters

def test_connection():
    # 指定正确的端口
    port = 57350
    gateway = JavaGateway(gateway_parameters=GatewayParameters(port=port))

    # 获取Java类的实例
    java_instance = gateway.entry_point

    # 调用Java方法
    java_instance.PythonAndJavaConnectionTester()

if __name__ == "__main__":
    test_connection()

# def on_press(key):
#     try:
#         print(f'Alphanumeric key pressed: {key.char}')
#     except AttributeError:
#         print(f'Special key pressed: {key}')


# def on_release(key):
#     print(f'Key released: {key}')
#     if key == keyboard.Key.esc:
#         # Stop listener
#         return False

# # Set up the listener
# with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()