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



section .bss
    digitSpace resb 100
    digitSpacePos resb 8

section .text
    global _start:

_start:
_addr0:
    ;; PUSH 34 ;;
    push 34

_addr1:
    ;; PUSH 35 ;;
    push 35

_addr2:
    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

_addr3:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr4:
    ;; PUSH 421 ;;
    push 421

_addr5:
    ;; PUSH 2 ;;
    push 2

_addr6:
    ;; SUB ;;
    pop rax
    pop rbx
    sub rbx, rax
    push rbx

_addr7:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr8:
    ;; PUSH 31 ;;
    push 31

_addr9:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr10:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
