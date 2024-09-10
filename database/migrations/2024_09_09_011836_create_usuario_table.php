<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('usuario', function (Blueprint $table) {
            $table->id();
            $table->string('Primer_Nombre');
            $table->string('Segundo_Nombre');
            $table->string('Primer_Apellido');
            $table->string('Segundo_Apellido');
            $table->string('Cedula');
            $table->enum('Rango', ['Gerente', 'Empleado']);
            $table->string('Email');
            $table->string('Celular');
            $table->string('Ciudad');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('usuario');
    }
};
