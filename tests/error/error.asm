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
    ;; PUSH 34 ;;
    push 34

    ;; PUSH 35 ;;
    push 35

    ;; ADD ;;
    pop rax
    pop rbx
    add rbx, rax
    push rbx

    ;; DUMP ;;
    pop rax
    call _printRAX

    ;; PUSH 31 ;;
    push 31

    ;; PUSH 21 ;;
    push 21

    ;; PUSH 21 ;;
    push 21

    ;; PUSH 21 ;;
    push 21

    ;; PUSH 21 ;;
    push 21

    ;; PUSH 21 ;;
    push 21

    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
