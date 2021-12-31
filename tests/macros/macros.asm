BITS 64
;; Subroutine to print an integer
;; in the rax register
_printRAX:
	mov rcx, digitSpace
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos], rcx

_printRAXLoop:
	mov rdx, 0
	mov rbx, 10
	div rbx
	push rax
	add rdx, 48

	mov rcx, [digitSpacePos]
	mov [rcx], dl
	inc rcx
	mov [digitSpacePos], rcx

	pop rax
	cmp rax, 0
	jne _printRAXLoop

_printRAXLoop2:
	mov rcx, [digitSpacePos]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos]
	dec rcx
	mov [digitSpacePos], rcx

	cmp rcx, digitSpace
	jge _printRAXLoop2

	ret



_mod9:
pop r14
_addr1:
    ;; PUSH 9 ;;
    push 9

_addr2:
    ;; DIVIDE ;;
    pop rbx
    pop rax
    mov rdx, 0
    idiv rbx
    push rax
    push rdx
_addr3:
    ;; swap ;;
    pop rax
    pop rbx
    push rax
    push rbx
_addr4:
    ;; POP ;;
    pop r13

_addr5:
push r14
ret
section .bss
    digitSpace resb 100
    digitSpacePos resb 8
    memory resb 800

section .text
    global _start:

_start:
_addr0:
_addr6:
    ;; PUSH 25 ;;
    push 25

_addr7:
call _mod9
_addr8:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr9:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
