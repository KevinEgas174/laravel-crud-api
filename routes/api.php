<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

use App\Http\Controllers\Api\usuarioController;

Route::get('/usuarios',[usuarioController::class, 'index']);

Route::get('/usuarios/{id}',[usuarioController::class, 'show'] );

Route::post('/usuarios',[usuarioController::class, 'store']);

Route::put('/usuarios/{id}',[usuarioController::class, 'update'] );

Route::patch('/usuarios/{id}',[usuarioController::class, 'updatePartial'] );

Route::delete('/usuarios/{id}',[usuarioController::class, 'destroy'] );