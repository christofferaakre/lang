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
    memory resb 800

section .text
    global _start:

_start:
_addr0:
    ;; PUSH 3 ;;
    push 3

_addr1:
    ;; PUSH 4 ;;
    push 4

_addr2:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr3:
    ;; EXIT ;;
    mov rax, 60
    pop rdi
    syscall

_addr4:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr5:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
