import Flutter
import UIKit

class SceneDelegate: UIResponder, UIWindowSceneDelegate {
    var window: UIWindow?
    private var engine: FlutterEngine?

    func scene(
        _ scene: UIScene,
        willConnectTo session: UISceneSession,
        options connectionOptions: UIScene.ConnectionOptions
    ) {
        guard let windowScene = scene as? UIWindowScene else { return }
        let engine = FlutterEngine(name: "io.flutter.qa")
        self.engine = engine
        engine.run()
        GeneratedPluginRegistrant.register(with: engine)
        let vc = FlutterViewController(engine: engine, nibName: nil, bundle: nil)
        let window = UIWindow(windowScene: windowScene)
        window.rootViewController = vc
        self.window = window
        window.makeKeyAndVisible()
        if let appDelegate = UIApplication.shared.delegate as? FlutterAppDelegate {
            appDelegate.window = window
        }
    }
}
