//fork from https://github.com/ekknod/logitech-cve
#ifndef MOUSE_H
#define MOUSE_H


#define GHUB_API __declspec(dllexport)
typedef int BOOL;

#ifdef __cplusplus
extern "C" {
#endif

	BOOL GHUB_API mouse_open(void);
	void GHUB_API mouse_close(void);
	void mouse_move(char button, char x, char y, char wheel);
	void GHUB_API moveR(int x, int y);
	void GHUB_API press(char button);
	void GHUB_API release();

#ifdef __cplusplus
}
#endif

#endif
