<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Usuario;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class usuarioController extends Controller
{
    public function index()
    {
        $usuarios = Usuario::all();

        //if($usuarios->isEmpty()) {
        //    $data = [
        //        'message' => 'No se encontraron usuarios',
        //        'status' => 200
        //    ];
        //    return response()->json($data, 404);
        //}

        $data = [
            'usuarios' => $usuarios,
            'status' => 200
        ];

        return response()->json($data, 200);
    }

    public function store(Request $request)
    {
        $validator = Validator::make($request->all(),[
            'Primer_Nombre' => 'required|max:50',
            'Segundo_Nombre' => 'required|max:50',
            'Primer_Apellido' => 'required|max:50',
            'Segundo_Apellido' => 'required|max:50',
            'Cedula' => 'required|digits:10|unique:usuario',
            'Rango' => 'required|in:Gerente,Empleado',
            'Email' => 'required|email|unique:usuario',
            'Celular' => 'required|digits:10|unique:usuario',
            'Ciudad' => 'required|max:50'
        ]);

        if ($validator->fails()){
            $data = [
                'message' => 'Error al validar los datos',
                'errors' => $validator->errors(),
                'status' => 400
            ];
            return response()->json($data, 400);
        }
        $usuario = Usuario::create([
            'Primer_Nombre' => $request->Primer_Nombre,
            'Segundo_Nombre' => $request->Segundo_Nombre,
            'Primer_Apellido' => $request->Primer_Apellido,
            'Segundo_Apellido' => $request->Segundo_Apellido,
            'Cedula' => $request->Cedula,
            'Rango' => $request->Rango,
            'Email' => $request->Email,
            'Celular' => $request->Celular,
            'Ciudad' => $request->Ciudad
        ]);

        if (!$usuario){
            $data = [
                'message' => 'Error al crear el usuario',
                'status' => 500
            ];
            return response()->json($data, 500);
        }
        
        $data = [
            'usuario' => $usuario,
            'message' => 'Usuario creado exitosamente',
            'status' => 201
        ];

        return response()->json($data, 201);
    }

    public function show($id)
    {
        $usuario = Usuario::find($id);

        if (!$usuario){
            $data = [
                'message' => 'No se encontró el usuario',
                'status' => 404
            ];
            return response()->json($data, 404);
        }

        $data = [
            'usuario' => $usuario,
            'status' => 200
        ];

        return response()->json($data, 200);
    }

    public function destroy($id)
    {
        $usuario = Usuario::find($id);

        if (!$usuario){
            $data = [
                'message' => 'No se encontró el usuario',
                'status' => 404
            ];
            return response()->json($data, 404);
        }

        if (!$usuario->delete()){
            $data = [
                'message' => 'Error al eliminar el usuario',
                'status' => 500
            ];
            return response()->json($data, 500);
        }

        $data = [
            'message' => 'Usuario eliminado exitosamente',
            'status' => 200
        ];

        return response()->json($data, 200);
    }

    public function update(Request $request, $id)
    {
        $usuario = Usuario::find($id);

        if (!$usuario){
            $data = [
                'message' => 'No se encontró el usuario',
                'status' => 404
            ];
            return response()->json($data, 404);
        }

        $validator = Validator::make($request->all(),[
            'Primer_Nombre' => 'required|max:50',
            'Segundo_Nombre' => 'required|max:50',
            'Primer_Apellido' => 'required|max:50',
            'Segundo_Apellido' => 'required|max:50',
            'Cedula' => 'required|digits:10|unique:usuario',
            'Rango' => 'required|in:Gerente,Empleado',
            'Email' => 'required|email|unique:usuario',
            'Celular' => 'required|digits:10|unique:usuario',
            'Ciudad' => 'required|max:50'
        ]);

        if ($validator->fails()) {
            $data = [
                'message' => 'Error al validar los datos',
                'errors' => $validator->errors(),
                'status' => 400
            ];
            return response()->json($data, 400);
        }

        $usuario->Primer_Nombre = $request->Primer_Nombre;
        $usuario->Segundo_Nombre = $request->Segundo_Nombre;
        $usuario->Primer_Apellido = $request->Primer_Apellido;
        $usuario->Segundo_Apellido = $request->Segundo_Apellido;
        $usuario->Cedula = $request->Cedula;
        $usuario->Rango = $request->Rango;
        $usuario->Email = $request->Email;
        $usuario->Celular = $request->Celular;
        $usuario->Ciudad = $request->Ciudad;

        $usuario->save();

        $data = [
            'message' => 'Usuario actualizado exitosamente',
            'usuario' => $usuario,
            'status' => 200
        ];

        return response()->json($data, 200);
    }

    public function updatePartial(Request $request, $id)
    {
        $usuario = Usuario::find($id);

        if (!$usuario){
            $data = [
                'message' => 'No se encontró el usuario',
                'status' => 404
            ];
            return response()->json($data, 404);
        }
        

        $validator = Validator::make($request->all(),[
            'Primer_Nombre' => 'max:50',
            'Segundo_Nombre' => 'max:50',
            'Primer_Apellido' => 'max:50',
            'Segundo_Apellido' => 'max:50',
            'Cedula' => 'digits:10|unique:usuario',
            'Rango' => 'in:Gerente,Empleado',
            'Email' => 'email|unique:usuario',
            'Celular' => 'digits:10|unique:usuario',
            'Ciudad' => 'max:50'
        ]);
        
        if ($validator->fails()) {
            $data = [
                'message' => 'Error al validar los datos',
                'errors' => $validator->errors(),
                'status' => 400
            ];
            return response()->json($data, 400);
        }

        if ($request->has('Primer_Nombre')){
            $usuario->Primer_Nombre = $request->Primer_Nombre;
        }

        if ($request->has('Segundo_Nombre')){
            $usuario->Segundo_Nombre = $request->Segundo_Nombre;
        }

        if ($request->has('Primer_Apellido')){
            $usuario->Primer_Apellido = $request->Primer_Apellido;
        }

        if ($request->has('Segundo_Apellido')){
            $usuario->Segundo_Apellido = $request->Segundo_Apellido;
        }
        
        if ($request->has('Cedula')){
            $usuario->Cedula = $request->Cedula;
        }

        if ($request->has('Rango')){
            $usuario->Rango = $request->Rango;
        }

        if ($request->has('Email')){
            $usuario->Email = $request->Email;
        }

        if ($request->has('Celular')){
            $usuario->Celular = $request->Celular;
        }

        if ($request->has('Ciudad')){
            $usuario->Ciudad = $request->Ciudad;
        }

        $usuario->save();

        $data = [
            'message' => 'Usuario actualizado exitosamente',
            'usuario' => $usuario,
            'status' => 200
        ];

        return response()->json($data, 200);
    }
}
