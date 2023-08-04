from app import Application, MenuWindow

if __name__ == "__main__":
    menu = MenuWindow(title = "Simulador - Configurações")
    menu.build()
    menu.run()

    if not menu.closed:
        process_scheduler = menu.get_process_scheduler()
        memory_manager = menu.get_memory_manager()

        application = Application(
            title = f"Simulador - {process_scheduler.name} Algorithm",
            real_memory_window_title = "Real Memory Table",
            virtual_memory_window_title = "Virtual Memory Table"
        )
        application.build()
        application.run(
            process_scheduler = process_scheduler,
            memory_manager = memory_manager,
            freeze_process_on_page_fault = menu.get_freeze_process_config(),
            generate_log_file = menu.get_log_config(),
            interval=menu.get_update_interval()
        )
