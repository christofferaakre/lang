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
    ;; PUSH 10 ;;
    push 10

_addr1:
    ;; PUSH 10 ;;
    push 10

_addr2:
    ;; > ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovg rdx, rbx
    push rdx
_addr3:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr4:
    ;; PUSH 100 ;;
    push 100

_addr5:
    ;; PUSH 5 ;;
    push 5

_addr6:
    ;; > ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovg rdx, rbx
    push rdx
_addr7:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr8:
    ;; PUSH 9 ;;
    push 9

_addr9:
    ;; PUSH 23 ;;
    push 23

_addr10:
    ;; > ;;
    pop rax
    pop rbx
    cmp rbx, rax
    mov rbx, 1
    mov rdx, 0
    cmovg rdx, rbx
    push rdx
_addr11:
    ;; DUMP ;;
    pop rax
    call _printRAX

_addr12:
    ;; EXIT ;; 
    mov rax, 60
    mov rdi, 0
    syscall
