_printRAX:
	mov rcx, digitSpace2
	mov rbx, 10
	mov [rcx], rbx
	inc rcx
	mov [digitSpacePos2], rcx

_printRAXLoop:
	mov rdx, 0
	mov rbx, 10
	div rbx
	push rax
	add rdx, 48

	mov rcx, [digitSpacePos2]
	mov [rcx], dl
	inc rcx
	mov [digitSpacePos2], rcx

	pop rax
	cmp rax, 0
	jne _printRAXLoop

_printRAXLoop2:
	mov rcx, [digitSpacePos2]

	mov rax, 1
	mov rdi, 1
	mov rsi, rcx
	mov rdx, 1
	syscall

	mov rcx, [digitSpacePos2]
	dec rcx
	mov [digitSpacePos2], rcx

	cmp rcx, digitSpace2
	jge _printRAXLoop2

	ret
