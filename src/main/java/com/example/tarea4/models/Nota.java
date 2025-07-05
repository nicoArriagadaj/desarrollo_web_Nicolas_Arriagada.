package com.example.tarea4.models;

import jakarta.persistence.*;

@Entity
@Table(name = "nota")
public class Nota {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)   
    private Integer id;

    @Column(name = "nota")
    private int valor;           

    @ManyToOne
    @JoinColumn(name = "actividad_id", nullable = false)  
    private Actividad actividad;

    public Nota() {}
    public Nota(int valor, Actividad actividad) {
        this.valor = valor;
        this.actividad = actividad;
    }
    public int getValor() { return valor; }
}
